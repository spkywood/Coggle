# pdf

tesseract-ocr poppler-utils

- 报错


```
第一个错误：tesseract_ocr.cpp:507:34: fatal error: leptonica/allheaders.h: No such file or directory
    compilation terminated.

解决办法：sudo apt install libleptonica-dev

第二个错误：tesseract_ocr.cpp:508:31: fatal error: tesseract/baseapi.h: No such file or directory
    compilation terminated.

解决办法：sudo apt install libtesseract-dev
```

