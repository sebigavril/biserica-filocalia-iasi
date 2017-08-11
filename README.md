# biserica-filocalia-iasi

### Biserica Filocalia Iasi

------

#### easislides2pdf
Simple script that creates a pdf file with songs exported from easislides in the default xml format.

###### How to run
 - pip install -r requirements.txt
 - python easislides2pdf.py inputFile.xml outputFile.pdf

 #### postLiveVideo
 Simple script that posts a live video to facebook & youtube

###### How to run
  - pip install -r requirements.txt
  - set environment variables:
    - FILOCALIA_FB_PAGE_ID
    - FILOCALIA_FB_TOKEN
    - FILOCALIA_YT_CLIENT_SECRETS_FILE
  - python postLiveVideo.py
