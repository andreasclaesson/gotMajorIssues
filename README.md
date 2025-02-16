# **gotMajorIssues** 🚀  
_A faster way to farm cards in NationStates using Python_

Original [gotIssues](https://github.com/jmikk/gotIssues) reworked as a way to farm issues & packs easily

## **Requirements**  
Before running the script, ensure you have the following:  

### **1. Install Required Python Libraries**  
You'll need [Python 3](https://apps.microsoft.com/detail/9ncvdn91xzqp?hl=en-us&gl=US) and `pip` to install `lxml`, `beautifulsoup4`, and `requests`. If you haven't installed `pip`, follow the guide [here](https://pip.pypa.io/en/stable/installation/).  

To install dependencies, run:  
```bash
pip install lxml beautifulsoup4 requests
```  

### **2. Recommended Tampermonkey Scripts**  
These scripts will speed up your farming process, located in [this repository](https://github.com/andreasclaesson/HNSS/blob/main/Farming/GotMajorIssues):  
- [**NsIssueCompactorRand.js**](https://github.com/andreasclaesson/HNSS/blob/main/Farming/GotMajorIssues/NsIssueCompactorRand.user.js) *(Hide everything except issue buttons and focus on a the middle option)*
- [**AutoCloseLogin.user.js**](https://github.com/andreasclaesson/HNSS/blob/main/Farming/GotMajorIssues/AutoCloseLogin.user.js) *(Auto-closes after nation has been logged in)*
- [**AutoClose.user.js**](https://github.com/andreasclaesson/HNSS/blob/main/Farming/GotMajorIssues/AutoClose.user.js) *(Auto-closes issue tabs when answered)*
- [**PackConditionalAutocloser.user.js**](https://github.com/Kractero/userscripts/blob/main/packConditionalAutocloser.user.js) (from Kractero) *(Auto-closes packs that does not contain legendary or card(s) with a market value over specified value)*

## **Setup & Usage**  
1. **Prepare Your Puppets**  
   - Add your puppet nations to a CSV file.  
   - Format:  
     ```csv
     MyPuppet,MySuperClever69Password
     MyOtherPuppet,IForgotThePasswordForThisOne
     ```
2. **Run the Scripts**  
   - **Step 1:** Run `python main.py` to generate all necessary text files with issues/packs for `generate.py` to use.  
   - **Step 2:** Execute `python generate.py` to create an HTML sheet with data.  

3. **Start Answering Issues/Packs**  
   - Open the generated HTML file and click through the links.  
   - **Spam enter until your keyboard is broken.**

## **⚠️ DISCLAIMER**  

### **Read Before Using Any Script**  
Using automation in NationStates comes with **responsibilities and risks**. Please follow the official scripting rules: [NationStates Scripting Rules](https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966).  

### **Rules for Script Usage:**  
✔️ **A human must press a button to trigger an event.**  
❌ You **CANNOT** use objects (e.g., a rock) to hold down a key.  
❌ You **CANNOT** automate continuous key presses.  

Using scripts improperly can **violate NationStates rules** (which is not fun) and result in penalties. Read and understand the code before using it. If unsure, consult the developer or a trusted source.  

**You are responsible for ensuring compliance with NationStates scripting regulations.**  


## **Contribute & Support**  
Feel free to contribute, report issues, or suggest improvements. 