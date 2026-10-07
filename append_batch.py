import pandas as pd

df_train = pd.read_csv("data/train_batch1.csv")
df_new   = pd.read_csv("data/train_batch2.csv")

original_size = len(df_train)
if original_size != len(df_new):
    raise SystemExit(
        "Expected the original batch1 to have the same size as batch2. "
        "The data may already have been appended; stopping to avoid duplication."
    )
df_updated = pd.concat([df_train, df_new], ignore_index=True)
df_updated.to_csv("data/train_batch1.csv", index=False)

print(f"Cap nhat du lieu: {original_size} -> {len(df_updated)} mau")
