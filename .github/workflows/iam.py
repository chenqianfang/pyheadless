name: HuaWeiIam

on:
#  push:
#    branches: [ master ]
  schedule:
    - cron: '50 0,2 * * *'

env:
  DING_TOKEN: ${{ secrets.DING_TOKEN }}

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.6'

    - name: requirements
      run: |
        pip3 install -r requirements.txt

    - name: Run 001
      run: |
        python3 main.py --client huawei_iam --username ${{ secrets.IAM_001_USERNAME }} --password ${{ secrets.IAM_001_PASSWORD }} --git-url ${{ secrets.IAM_001_GIT }}
