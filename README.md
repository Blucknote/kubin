
# Kubin: Web-GUI for [Kandinsky 2.1](https://github.com/ai-forever/Kandinsky-2/)


## Disclaimer

WIP - DO NOT USE 🛑
<br>

## Features

Currently only basic functions implemented (nothing new compared to [official notebooks](https://github.com/ai-forever/Kandinsky-2/tree/main/notebooks)):
* txt2img
* img2img
* mixing
* inpainting 


## Screenshots (outdated)
<details> 
<summary>Expand</summary>

### txt2img
	
![img](/sshots/t2i.png)
	
<br>

### img2img
	
![img](/sshots/i2i.png)

<br>

### mixing
	
![img](/sshots/mix.png)

<br>
	
### inpainting
    
![img](/sshots/inpaint.png)
	
</details>
<br>

## Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1lx4lQS61hYb02BSoAoJUAVwPr7PhhkJt)
<br>

## Roadmap xD

* Upscaling
* Outpainting
* Extension support 
* Fine-tuning ([textual inversion](https://github.com/TheDenk/Kandinsky-2-textual-inversion) 👀)
* Advanced prompt syntax
* Interrogation
* More samplers
* SAM/Grounded SAM 🤩
* Animation
* ControlNet 🙏
* Inference optimization: memory 📉 + speed 📈
* TODO: insert another features I will never get done
<br>

## Local installation (Windows 10, Python 3.10, PowerShell)

```
git clone https://github.com/seruva19/kubin
cd kubin
py -m venv venv
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
py src/kubin.py
```
GUI then should be available at http://127.0.0.1:7860/
<br>
To update to latest version, use
```
git pull

```

## Documentation

Maybe later 🤷
