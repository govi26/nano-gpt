import argparse
import os
import torch

from peft import AutoPeftModelForCausalLM, LoraConfig
from transformers import AutoTokenizer, TrainingArguments
from datasets import load_dataset
from trl import DPOTrainer


def get_stack_exchange_paired(
    data_dir="data/rl",
    sanity_check=False,
    cache_dir=None,
    num_proc=24,
):

  dataset = load_dataset(
    "lvwerra/stack-exchange-paired",
    split="train",
    cache_dir=cache_dir,
    data_dir=data_dir,
  )
  original_columns = dataset.column_names

  if sanity_check:
    dataset = dataset.select(range(min(len(dataset), 1000)))

  def return_prompt_and_responses(samples):
    return {
      "prompt": ["Question: " + question + "\n\nAnswer: " for question in samples["question"]],
      "chosen": samples["response_j"],
      "rejected": samples["response_k"],
    }

  return dataset.map(
    return_prompt_and_responses,
    batched=True,
    num_proc=num_proc,
    remove_columns=original_columns,
  )

def dpo_training(script_args):
  # 1. load a pretrained model
  model = AutoPeftModelForCausalLM.from_pretrained(
    script_args.model_name_or_path,
    low_cpu_mem_usage=True,
    torch_dtype=torch.float16,
    load_in_4bit=True,
    is_trainable=True,
  )
  model_ref = AutoPeftModelForCausalLM.from_pretrained(
    script_args.model_name_or_path,
    low_cpu_mem_usage=True,
    torch_dtype=torch.float16,
    load_in_4bit=True,
  )

  tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
  tokenizer.pad_token = tokenizer.eos_token

  # 2. Load the Stack-exchange paired dataset
  train_dataset = get_stack_exchange_paired(
    data_dir="data/rl", sanity_check=script_args.sanity_check
  )
  train_dataset = train_dataset.filter(
    lambda x: len(x["prompt"]) + len(x["chosen"]) <= script_args.max_length
              and len(x["prompt"]) + len(x["rejected"]) <= script_args.max_length
  )

  # 3. Load evaluation dataset
  eval_dataset = get_stack_exchange_paired(
    data_dir="data/evaluation", sanity_check=True
  )
  eval_dataset = eval_dataset.filter(
    lambda x: len(x["prompt"]) + len(x["chosen"]) <= script_args.max_length
              and len(x["prompt"]) + len(x["rejected"]) <= script_args.max_length
  )

  # 4. initialize training arguments:
  training_args = TrainingArguments(
    per_device_train_batch_size=script_args.per_device_train_batch_size,
    per_device_eval_batch_size=script_args.per_device_eval_batch_size,
    max_steps=script_args.max_steps,
    logging_steps=script_args.logging_steps,
    save_steps=script_args.save_steps,
    gradient_accumulation_steps=script_args.gradient_accumulation_steps,
    gradient_checkpointing=script_args.gradient_checkpointing,
    learning_rate=script_args.learning_rate,
    evaluation_strategy="steps",
    eval_steps=script_args.eval_steps,
    output_dir=script_args.output_dir,
    report_to=script_args.report_to,
    lr_scheduler_type=script_args.lr_scheduler_type,
    warmup_steps=script_args.warmup_steps,
    optim=script_args.optimizer_type,
    bf16=True,
    remove_unused_columns=False,
    run_name="dpo_llama2",
  )

  peft_config = LoraConfig(
    r=script_args.lora_r,
    lora_alpha=script_args.lora_alpha,
    lora_dropout=script_args.lora_dropout,
    target_modules=[
      "q_proj",
      "v_proj",
      "k_proj",
      "out_proj",
      "fc_in",
      "fc_out",
      "wte",
    ],
    bias="none",
    task_type="CAUSAL_LM",
  )

  # 5. initialize the DPO trainer
  dpo_trainer = DPOTrainer(
    model,
    model_ref,
    args=training_args,
    beta=script_args.beta,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    peft_config=peft_config,
    max_prompt_length=script_args.max_prompt_length,
    max_length=script_args.max_length,
  )

  # 6. train
  dpo_trainer.train()
  dpo_trainer.save_model(script_args.output_dir)

  # 7. save
  output_path = os.path.join(script_args.output_dir, "dpo_trained")
  dpo_trainer.model.save_pretrained(output_path)


def main():
  script_args = read_args()
  dpo_training(script_args)


def read_args():
  parser = argparse.ArgumentParser(description="dpo training")

  parser.add_argument('--beta', type=float, help='the beta parameter for DPO loss')
  parser.add_argument('--model_name_or_path', type=str, help='the location of the SFT model name or path')
  parser.add_argument('--learning_rate', type=float, help='optimizer learning rate')
  parser.add_argument('--lr_scheduler_type', type=str, help='the lr scheduler type')
  parser.add_argument('--warmup_steps', type=int, help='the number of warmup steps')
  parser.add_argument('--weight_decay', type=float, help='the weight decay')
  parser.add_argument('--optimizer_type', type=str, help='the optimizer type')
  parser.add_argument('--per_device_train_batch_size', type=int, help='train batch size per device')
  parser.add_argument('--per_device_eval_batch_size', type=int, help='eval batch size per device')
  parser.add_argument('--gradient_accumulation_steps', type=int, help='the number of gradient accumulation steps')
  parser.add_argument('--gradient_checkpointing', type=bool, help='whether to use gradient checkpointing')
  parser.add_argument('--lora_alpha', type=float, help='the lora alpha parameter')
  parser.add_argument('--lora_dropout', type=float, help='the lora dropout parameter')
  parser.add_argument('--lora_r', type=int, help='the lora r parameter')
  parser.add_argument('--max_prompt_length', type=int, help='the maximum prompt length')
  parser.add_argument('--max_length', type=int, help='the maximum sequence length')
  parser.add_argument('--max_steps', type=int, help='max number of training steps')
  parser.add_argument('--logging_steps', type=int, help='the logging frequency')
  parser.add_argument('--save_steps', type=int, help='the saving frequency')
  parser.add_argument('--eval_steps', type=int, help='the evaluation frequency')
  parser.add_argument('--output_dir', type=str, help='the output directory')
  parser.add_argument('--log_freq', type=int, help='the logging frequency')
  parser.add_argument('--sanity_check', type=bool, help='only train on 1000 samples')
  parser.add_argument('--report_to', type=str, help='The list of integrations to report the results and logs to. Supported platforms are "azure_ml","comet_ml", "mlflow", "neptune", "tensorboard","clearml" and "wandb". Use "all" to report to all integrations installed, "none" for no integrations.')
  parser.add_argument('--ignore_bias_buffers', type=bool, help='fix for DDP issues with LM bias/mask buffers - invalid scalar type,inplace operation. See https://github.com/huggingface/transformers/issues/22482#issuecomment-1595790992')

  parser.set_defaults(
    beta=0.1,
    model_name_or_path="./persist_complete_for_dpo",
    learning_rate=5e-4,
    lr_scheduler_type="cosine",
    warmup_steps=100,
    weight_decay=0.05,
    optimizer_type="paged_adamw_32bit",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=4,
    gradient_checkpointing=True,
    lora_alpha=16,
    lora_dropout=0.05,
    lora_r=8,
    max_prompt_length=512,
    max_length=1024,
    max_steps=1000,
    logging_steps=10,
    save_steps=100,
    eval_steps=100,
    output_dir="./results",
    log_freq=1,
    sanity_check=False,
    report_to="wandb",
    ignore_bias_buffers=False,
  )

  return parser.parse_args()


if __name__ == "__main__":
  main()
