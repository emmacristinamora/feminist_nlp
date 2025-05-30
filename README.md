# 📚 Feminist Literature NLP

This project applies natural language processing (NLP) and deep learning to explore feminist themes, character agency, emotion, and authorial style in literary texts. It combines traditional techniques like TF-IDF and topic modeling with transformer-based models like BERT and DistilBERT.

---

## 🎯 Project Goals

1. **Preprocess and tokenize literary texts** to prepare for analysis  
2. **Identify and track characters** through Named Entity Recognition and coreference resolution  
3. **Measure agency** of women characters using syntactic analysis  
4. **Trace feminist themes** (e.g., marriage, work, independence) over time  
5. **Classify emotion and tone** around gendered terms  
6. **Compare authorial style** using stylometric techniques  
7. *(Optional)* **Prompt large language models (LLMs)** to extract interpretive insights  

---

## 🧪 Methods Overview

### 1. Data Preparation & Preprocessing

- **Objective**: Clean, tokenize, and lemmatize text  
- **Tools**: `spaCy`, `nltk`  
- **Includes**: Lowercasing, punctuation/stopword removal, sentence segmentation

---

### 2. Named Entity Recognition + Coreference Resolution

- **Objective**: Detect PERSON entities and resolve pronouns  
- **Tools**: `spaCy`, `neuralcoref` or `AllenNLP`

---

### 3. Character Agency Analysis (MARA)

- **Objective**: Quantify what women characters do vs. what is done to them  
- **Tools**: POS tagging, dependency parsing, verb dictionary

---

### 4. Thematic Analysis (EMMA)

- **Objective**: Identify feminist themes using unsupervised topic modeling  
- **Tools**: `TF-IDF`, `BERTopic`, `LDA`, KWIC tools

---

### 5. Emotion & Tone Classification (EMMA)

- **Objective**: Understand emotional framing of gendered roles  
- **Tools**: `transformers`, GoEmotions labels, DistilBERT

---

### 6. Stylometric Analysis (MERVE)

- **Objective**: Compare authors (e.g., Austen vs. Woolf) by writing style  
- **Tools**: `TF-IDF`, `doc2vec`, `BERT`, `UMAP`, `SVM`

---

### 7. Optional: Prompting with LLMs

- **Objective**: Use GPT-3.5+ models for zero/few-shot classification or role extraction  
- **Tools**: `OpenAI API`

---

## ⚙️ Installation & Setup

### 📁 Clone the Repository

```bash
git clone https://github.com/emmacristinamora/feminist-literature-nlp.git
cd feminist-literature-nlp