{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "a196cb36-dbb2-4642-b037-4f48ca659383",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current\n",
      "                                 Dload  Upload   Total   Spent    Left  Speed\n",
      "\n",
      "  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0\n",
      "100 1089k  100 1089k    0     0  2033k      0 --:--:-- --:--:-- --:--:-- 2047k\n"
     ]
    }
   ],
   "source": [
    "# We always start with a dataset to train on. Let's download the tiny shakespeare dataset\n",
    "!curl -O https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "86251c44-89a6-4803-8086-e83915618d59",
   "metadata": {},
   "outputs": [],
   "source": [
    "# read it in to inspect it\n",
    "with open('input.txt', 'r', encoding='utf-8') as f:\n",
    "    text = f.read()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "91a5f13b-e10c-437a-b7d6-eedb044f5e71",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "length of dataset in characters:  1115394\n"
     ]
    }
   ],
   "source": [
    "print(\"length of dataset in characters: \", len(text))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "14e64c46-bb9c-4e33-b16d-1b47c9cea484",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "First Citizen:\n",
      "Before we proceed any further, hear me speak.\n",
      "\n",
      "All:\n",
      "Speak, speak.\n",
      "\n",
      "First Citizen:\n",
      "You are all resolved rather to die than to famish?\n",
      "\n",
      "All:\n",
      "Resolved. resolved.\n",
      "\n",
      "First Citizen:\n",
      "First, you know Caius Marcius is chief enemy to the people.\n",
      "\n",
      "All:\n",
      "We know't, we know't.\n",
      "\n",
      "First Citizen:\n",
      "Let us kill him, and we'll have corn at our own price.\n",
      "Is't a verdict?\n",
      "\n",
      "All:\n",
      "No more talking on't; let it be done: away, away!\n",
      "\n",
      "Second Citizen:\n",
      "One word, good citizens.\n",
      "\n",
      "First Citizen:\n",
      "We are accounted poor citizens, the patricians good.\n",
      "What authority surfeits on would relieve us: if they\n",
      "would yield us but the superfluity, while it were\n",
      "wholesome, we might guess they relieved us humanely;\n",
      "but they think we are too dear: the leanness that\n",
      "afflicts us, the object of our misery, is as an\n",
      "inventory to particularise their abundance; our\n",
      "sufferance is a gain to them Let us revenge this with\n",
      "our pikes, ere we become rakes: for the gods know I\n",
      "speak this in hunger for bread, not in thirst for revenge.\n",
      "\n",
      "\n"
     ]
    }
   ],
   "source": [
    "# let's look at the first 1000 characters\n",
    "print(text[:1000])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "fbcb2292-fe37-4685-9962-f369693441c5",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      " !$&',-.3:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\n",
      "65\n"
     ]
    }
   ],
   "source": [
    "# here are all the unique characters that occur in this text\n",
    "chars = sorted(list(set(text)))\n",
    "vocab_size = len(chars)\n",
    "print(''.join(chars))\n",
    "print(vocab_size)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "e446ed6c-6678-42ed-9772-2680077c55fd",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[46, 47, 47, 1, 58, 46, 43, 56, 43]\n",
      "hii there\n"
     ]
    }
   ],
   "source": [
    "# create a mapping from characters to integers\n",
    "stoi = { ch:i for i,ch in enumerate(chars) }\n",
    "itos = { i:ch for i,ch in enumerate(chars) }\n",
    "encode = lambda s: [stoi[c] for c in s] # encoder: take a string, output a list of integers\n",
    "decode = lambda l: ''.join([itos[i] for i in l]) # decoder: take a list of integers, output a string\n",
    "\n",
    "print(encode(\"hii there\"))\n",
    "print(decode(encode(\"hii there\")))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "b3259ac7-5d8f-4033-b12f-1293466497da",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "torch.Size([1115394]) torch.int64\n",
      "tensor([18, 47, 56, 57, 58,  1, 15, 47, 58, 47, 64, 43, 52, 10,  0, 14, 43, 44,\n",
      "        53, 56, 43,  1, 61, 43,  1, 54, 56, 53, 41, 43, 43, 42,  1, 39, 52, 63,\n",
      "         1, 44, 59, 56, 58, 46, 43, 56,  6,  1, 46, 43, 39, 56,  1, 51, 43,  1,\n",
      "        57, 54, 43, 39, 49,  8,  0,  0, 13, 50, 50, 10,  0, 31, 54, 43, 39, 49,\n",
      "         6,  1, 57, 54, 43, 39, 49,  8,  0,  0, 18, 47, 56, 57, 58,  1, 15, 47,\n",
      "        58, 47, 64, 43, 52, 10,  0, 37, 53, 59,  1, 39, 56, 43,  1, 39, 50, 50,\n",
      "         1, 56, 43, 57, 53, 50, 60, 43, 42,  1, 56, 39, 58, 46, 43, 56,  1, 58,\n",
      "        53,  1, 42, 47, 43,  1, 58, 46, 39, 52,  1, 58, 53,  1, 44, 39, 51, 47,\n",
      "        57, 46, 12,  0,  0, 13, 50, 50, 10,  0, 30, 43, 57, 53, 50, 60, 43, 42,\n",
      "         8,  1, 56, 43, 57, 53, 50, 60, 43, 42,  8,  0,  0, 18, 47, 56, 57, 58,\n",
      "         1, 15, 47, 58, 47, 64, 43, 52, 10,  0, 18, 47, 56, 57, 58,  6,  1, 63,\n",
      "        53, 59,  1, 49, 52, 53, 61,  1, 15, 39, 47, 59, 57,  1, 25, 39, 56, 41,\n",
      "        47, 59, 57,  1, 47, 57,  1, 41, 46, 47, 43, 44,  1, 43, 52, 43, 51, 63,\n",
      "         1, 58, 53,  1, 58, 46, 43,  1, 54, 43, 53, 54, 50, 43,  8,  0,  0, 13,\n",
      "        50, 50, 10,  0, 35, 43,  1, 49, 52, 53, 61,  5, 58,  6,  1, 61, 43,  1,\n",
      "        49, 52, 53, 61,  5, 58,  8,  0,  0, 18, 47, 56, 57, 58,  1, 15, 47, 58,\n",
      "        47, 64, 43, 52, 10,  0, 24, 43, 58,  1, 59, 57,  1, 49, 47, 50, 50,  1,\n",
      "        46, 47, 51,  6,  1, 39, 52, 42,  1, 61, 43,  5, 50, 50,  1, 46, 39, 60,\n",
      "        43,  1, 41, 53, 56, 52,  1, 39, 58,  1, 53, 59, 56,  1, 53, 61, 52,  1,\n",
      "        54, 56, 47, 41, 43,  8,  0, 21, 57,  5, 58,  1, 39,  1, 60, 43, 56, 42,\n",
      "        47, 41, 58, 12,  0,  0, 13, 50, 50, 10,  0, 26, 53,  1, 51, 53, 56, 43,\n",
      "         1, 58, 39, 50, 49, 47, 52, 45,  1, 53, 52,  5, 58, 11,  1, 50, 43, 58,\n",
      "         1, 47, 58,  1, 40, 43,  1, 42, 53, 52, 43, 10,  1, 39, 61, 39, 63,  6,\n",
      "         1, 39, 61, 39, 63,  2,  0,  0, 31, 43, 41, 53, 52, 42,  1, 15, 47, 58,\n",
      "        47, 64, 43, 52, 10,  0, 27, 52, 43,  1, 61, 53, 56, 42,  6,  1, 45, 53,\n",
      "        53, 42,  1, 41, 47, 58, 47, 64, 43, 52, 57,  8,  0,  0, 18, 47, 56, 57,\n",
      "        58,  1, 15, 47, 58, 47, 64, 43, 52, 10,  0, 35, 43,  1, 39, 56, 43,  1,\n",
      "        39, 41, 41, 53, 59, 52, 58, 43, 42,  1, 54, 53, 53, 56,  1, 41, 47, 58,\n",
      "        47, 64, 43, 52, 57,  6,  1, 58, 46, 43,  1, 54, 39, 58, 56, 47, 41, 47,\n",
      "        39, 52, 57,  1, 45, 53, 53, 42,  8,  0, 35, 46, 39, 58,  1, 39, 59, 58,\n",
      "        46, 53, 56, 47, 58, 63,  1, 57, 59, 56, 44, 43, 47, 58, 57,  1, 53, 52,\n",
      "         1, 61, 53, 59, 50, 42,  1, 56, 43, 50, 47, 43, 60, 43,  1, 59, 57, 10,\n",
      "         1, 47, 44,  1, 58, 46, 43, 63,  0, 61, 53, 59, 50, 42,  1, 63, 47, 43,\n",
      "        50, 42,  1, 59, 57,  1, 40, 59, 58,  1, 58, 46, 43,  1, 57, 59, 54, 43,\n",
      "        56, 44, 50, 59, 47, 58, 63,  6,  1, 61, 46, 47, 50, 43,  1, 47, 58,  1,\n",
      "        61, 43, 56, 43,  0, 61, 46, 53, 50, 43, 57, 53, 51, 43,  6,  1, 61, 43,\n",
      "         1, 51, 47, 45, 46, 58,  1, 45, 59, 43, 57, 57,  1, 58, 46, 43, 63,  1,\n",
      "        56, 43, 50, 47, 43, 60, 43, 42,  1, 59, 57,  1, 46, 59, 51, 39, 52, 43,\n",
      "        50, 63, 11,  0, 40, 59, 58,  1, 58, 46, 43, 63,  1, 58, 46, 47, 52, 49,\n",
      "         1, 61, 43,  1, 39, 56, 43,  1, 58, 53, 53,  1, 42, 43, 39, 56, 10,  1,\n",
      "        58, 46, 43,  1, 50, 43, 39, 52, 52, 43, 57, 57,  1, 58, 46, 39, 58,  0,\n",
      "        39, 44, 44, 50, 47, 41, 58, 57,  1, 59, 57,  6,  1, 58, 46, 43,  1, 53,\n",
      "        40, 48, 43, 41, 58,  1, 53, 44,  1, 53, 59, 56,  1, 51, 47, 57, 43, 56,\n",
      "        63,  6,  1, 47, 57,  1, 39, 57,  1, 39, 52,  0, 47, 52, 60, 43, 52, 58,\n",
      "        53, 56, 63,  1, 58, 53,  1, 54, 39, 56, 58, 47, 41, 59, 50, 39, 56, 47,\n",
      "        57, 43,  1, 58, 46, 43, 47, 56,  1, 39, 40, 59, 52, 42, 39, 52, 41, 43,\n",
      "        11,  1, 53, 59, 56,  0, 57, 59, 44, 44, 43, 56, 39, 52, 41, 43,  1, 47,\n",
      "        57,  1, 39,  1, 45, 39, 47, 52,  1, 58, 53,  1, 58, 46, 43, 51,  1, 24,\n",
      "        43, 58,  1, 59, 57,  1, 56, 43, 60, 43, 52, 45, 43,  1, 58, 46, 47, 57,\n",
      "         1, 61, 47, 58, 46,  0, 53, 59, 56,  1, 54, 47, 49, 43, 57,  6,  1, 43,\n",
      "        56, 43,  1, 61, 43,  1, 40, 43, 41, 53, 51, 43,  1, 56, 39, 49, 43, 57,\n",
      "        10,  1, 44, 53, 56,  1, 58, 46, 43,  1, 45, 53, 42, 57,  1, 49, 52, 53,\n",
      "        61,  1, 21,  0, 57, 54, 43, 39, 49,  1, 58, 46, 47, 57,  1, 47, 52,  1,\n",
      "        46, 59, 52, 45, 43, 56,  1, 44, 53, 56,  1, 40, 56, 43, 39, 42,  6,  1,\n",
      "        52, 53, 58,  1, 47, 52,  1, 58, 46, 47, 56, 57, 58,  1, 44, 53, 56,  1,\n",
      "        56, 43, 60, 43, 52, 45, 43,  8,  0,  0])\n"
     ]
    }
   ],
   "source": [
    "# let's now encode the entire text dataset and store it into a torch.Tensor\n",
    "import torch # we use PyTorch: https://pytorch.org\n",
    "data = torch.tensor(encode(text), dtype=torch.long)\n",
    "print(data.shape, data.dtype)\n",
    "print(data[:1000]) # the 1000 characters we looked at earier will to the GPT look like this"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "05e3e583-8f80-4305-ab9d-e1cecaeba707",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Let's now split up the data into train and validation sets\n",
    "n = int(0.9*len(data)) # first 90% will be train, rest val\n",
    "train_data = data[:n]\n",
    "val_data = data[n:]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "3317a5bb-732a-405d-a10c-6c75cd5f43fa",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "tensor([18, 47, 56, 57, 58,  1, 15, 47, 58])"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "block_size = 8\n",
    "train_data[:block_size+1]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "fcbf0a6e-ae2f-4bcd-a4e5-0b966dce6841",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "when input is tensor([18]) the target: 47\n",
      "when input is tensor([18, 47]) the target: 56\n",
      "when input is tensor([18, 47, 56]) the target: 57\n",
      "when input is tensor([18, 47, 56, 57]) the target: 58\n",
      "when input is tensor([18, 47, 56, 57, 58]) the target: 1\n",
      "when input is tensor([18, 47, 56, 57, 58,  1]) the target: 15\n",
      "when input is tensor([18, 47, 56, 57, 58,  1, 15]) the target: 47\n",
      "when input is tensor([18, 47, 56, 57, 58,  1, 15, 47]) the target: 58\n"
     ]
    }
   ],
   "source": [
    "x = train_data[:block_size]\n",
    "y = train_data[1:block_size+1]\n",
    "for t in range(block_size):\n",
    "    context = x[:t+1]\n",
    "    target = y[t]\n",
    "    print(f\"when input is {context} the target: {target}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "f56d0f34-c36d-49ce-b6cb-0d3a064952b0",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "inputs:\n",
      "torch.Size([4, 8])\n",
      "tensor([[24, 43, 58,  5, 57,  1, 46, 43],\n",
      "        [44, 53, 56,  1, 58, 46, 39, 58],\n",
      "        [52, 58,  1, 58, 46, 39, 58,  1],\n",
      "        [25, 17, 27, 10,  0, 21,  1, 54]])\n",
      "targets:\n",
      "torch.Size([4, 8])\n",
      "tensor([[43, 58,  5, 57,  1, 46, 43, 39],\n",
      "        [53, 56,  1, 58, 46, 39, 58,  1],\n",
      "        [58,  1, 58, 46, 39, 58,  1, 46],\n",
      "        [17, 27, 10,  0, 21,  1, 54, 39]])\n",
      "----\n",
      "when input is [24] the target: 43\n",
      "when input is [24, 43] the target: 58\n",
      "when input is [24, 43, 58] the target: 5\n",
      "when input is [24, 43, 58, 5] the target: 57\n",
      "when input is [24, 43, 58, 5, 57] the target: 1\n",
      "when input is [24, 43, 58, 5, 57, 1] the target: 46\n",
      "when input is [24, 43, 58, 5, 57, 1, 46] the target: 43\n",
      "when input is [24, 43, 58, 5, 57, 1, 46, 43] the target: 39\n",
      "when input is [44] the target: 53\n",
      "when input is [44, 53] the target: 56\n",
      "when input is [44, 53, 56] the target: 1\n",
      "when input is [44, 53, 56, 1] the target: 58\n",
      "when input is [44, 53, 56, 1, 58] the target: 46\n",
      "when input is [44, 53, 56, 1, 58, 46] the target: 39\n",
      "when input is [44, 53, 56, 1, 58, 46, 39] the target: 58\n",
      "when input is [44, 53, 56, 1, 58, 46, 39, 58] the target: 1\n",
      "when input is [52] the target: 58\n",
      "when input is [52, 58] the target: 1\n",
      "when input is [52, 58, 1] the target: 58\n",
      "when input is [52, 58, 1, 58] the target: 46\n",
      "when input is [52, 58, 1, 58, 46] the target: 39\n",
      "when input is [52, 58, 1, 58, 46, 39] the target: 58\n",
      "when input is [52, 58, 1, 58, 46, 39, 58] the target: 1\n",
      "when input is [52, 58, 1, 58, 46, 39, 58, 1] the target: 46\n",
      "when input is [25] the target: 17\n",
      "when input is [25, 17] the target: 27\n",
      "when input is [25, 17, 27] the target: 10\n",
      "when input is [25, 17, 27, 10] the target: 0\n",
      "when input is [25, 17, 27, 10, 0] the target: 21\n",
      "when input is [25, 17, 27, 10, 0, 21] the target: 1\n",
      "when input is [25, 17, 27, 10, 0, 21, 1] the target: 54\n",
      "when input is [25, 17, 27, 10, 0, 21, 1, 54] the target: 39\n"
     ]
    }
   ],
   "source": [
    "torch.manual_seed(1337)\n",
    "batch_size = 4 # how many independent sequences will we process in parallel?\n",
    "block_size = 8 # what is the maximum context length for predictions?\n",
    "\n",
    "def get_batch(split):\n",
    "    # generate a small batch of data of inputs x and targets y\n",
    "    data = train_data if split == 'train' else val_data\n",
    "    ix = torch.randint(len(data) - block_size, (batch_size,))\n",
    "    x = torch.stack([data[i:i+block_size] for i in ix])\n",
    "    y = torch.stack([data[i+1:i+block_size+1] for i in ix])\n",
    "    return x, y\n",
    "\n",
    "xb, yb = get_batch('train')\n",
    "print('inputs:')\n",
    "print(xb.shape)\n",
    "print(xb)\n",
    "print('targets:')\n",
    "print(yb.shape)\n",
    "print(yb)\n",
    "\n",
    "print('----')\n",
    "\n",
    "for b in range(batch_size): # batch dimension\n",
    "    for t in range(block_size): # time dimension\n",
    "        context = xb[b, :t+1]\n",
    "        target = yb[b,t]\n",
    "        print(f\"when input is {context.tolist()} the target: {target}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "88d13d33-7a7a-436c-a8a0-0f1a8abecf95",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "tensor([[24, 43, 58,  5, 57,  1, 46, 43],\n",
      "        [44, 53, 56,  1, 58, 46, 39, 58],\n",
      "        [52, 58,  1, 58, 46, 39, 58,  1],\n",
      "        [25, 17, 27, 10,  0, 21,  1, 54]])\n"
     ]
    }
   ],
   "source": [
    "print(xb) # input to transformer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "4a258714-b738-42f7-aa5c-002114c252e1",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "torch.Size([32, 65])\n",
      "tensor(4.8786, grad_fn=<NllLossBackward0>)\n",
      "\n",
      "Sr?qP-QWktXoL&jLDJgOLVz'RIoDqHdhsV&vLLxatjscMpwLERSPyao.qfzs$Ys$zF-w,;eEkzxjgCKFChs!iWW.ObzDnxA Ms$3\n"
     ]
    }
   ],
   "source": [
    "import torch\n",
    "import torch.nn as nn\n",
    "from torch.nn import functional as F\n",
    "torch.manual_seed(1337)\n",
    "\n",
    "class BigramLanguageModel(nn.Module):\n",
    "\n",
    "    def __init__(self, vocab_size):\n",
    "        super().__init__()\n",
    "        # each token directly reads off the logits for the next token from a lookup table\n",
    "        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)\n",
    "\n",
    "    def forward(self, idx, targets=None):\n",
    "        logits = self.token_embedding_table(idx) # (B,T,C)\n",
    "\n",
    "        if targets is None:\n",
    "            loss = None\n",
    "        else:\n",
    "            # idx and targets are both (B,T) tensor of integers (2D arrays)\n",
    "            B,T,C = logits.shape\n",
    "            logits = logits.view(B*T, C)\n",
    "            targets = targets.view(B*T)\n",
    "            loss = F.cross_entropy(logits, targets)\n",
    "        return logits, loss\n",
    "\n",
    "\n",
    "    def generate(self, idx, max_new_tokens):\n",
    "        # idx is (B, T) array of indices in the current context\n",
    "        for _ in range(max_new_tokens):\n",
    "            # get the predictions\n",
    "            logits, loss = self(idx)\n",
    "            # focus only on the last time step\n",
    "            logits = logits[:, -1, :] # becomes (B, C)\n",
    "            # apply softmax to get probabilities\n",
    "            probs = F.softmax(logits, dim=-1) # (B, C)\n",
    "            # sample from the distribution\n",
    "            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)\n",
    "            # append sampled index to the running sequence\n",
    "            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)\n",
    "        return idx\n",
    "\n",
    "m = BigramLanguageModel(vocab_size)\n",
    "logits, loss = m(xb, yb)\n",
    "print(logits.shape)\n",
    "print(loss)\n",
    "\n",
    "print(decode(m.generate(idx = torch.zeros((1, 1), dtype=torch.long), max_new_tokens=100)[0].tolist()))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "656ca064-dc1d-437f-b438-f6dff464ddbd",
   "metadata": {},
   "outputs": [],
   "source": [
    "#pytorch optimizer\n",
    "optimizer = torch.optim.AdamW(m.parameters(), lr=1e-3)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "id": "d72407cd-ca72-42b7-9957-33b270b96d7b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2.465181350708008\n"
     ]
    }
   ],
   "source": [
    "batch_size = 32\n",
    "for steps in range(10000): # increase number of steps for good results...\n",
    "\n",
    "    # sample a batch of data\n",
    "    xb, yb = get_batch('train')\n",
    "\n",
    "    # evaluate the loss\n",
    "    logits, loss = m(xb, yb)\n",
    "    optimizer.zero_grad(set_to_none=True)\n",
    "    loss.backward()\n",
    "    optimizer.step()\n",
    "\n",
    "print(loss.item())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "id": "c4671d42-8195-41b8-991c-dc97c71d96f4",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "He g sounomy.\n",
      "\n",
      "TICLKINourushes t bladoonju cie st t tree IIOLENREThand t, aghath,\n",
      "MI: Fol'storevend os tho geat; tisheer lid al'st bal l are, tour bu olll pt my.\n",
      "FR tr beser fare, wer\n",
      "\n",
      "Whoto y oo nd plerlethor myseres: omathita illt w,\n",
      "Taley myocomeat nethest,\n",
      "NGLAnd,\n",
      "Anen!\n",
      "3QUMI; frthily, my Ise IIAn,\n",
      "Five.\n",
      "BOUCARI ke y vese o ye foy VENRYBireswo n\n",
      "\n",
      "ABaXqusune y my n;\n",
      "'e w: t w; MELULo INen meng te t:\n",
      "in ticothingh, much s ESThondiryrs y ve:\n",
      "\n",
      "The thafenda merar\n",
      "WAng, aothace Pay, ty---\n",
      "Tu whea \n"
     ]
    }
   ],
   "source": [
    "print(decode(m.generate(idx = torch.zeros((1, 1), dtype=torch.long), max_new_tokens=500)[0].tolist()))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "32cea4d3-3c83-4a20-8e43-5ed3a8bc2867",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
