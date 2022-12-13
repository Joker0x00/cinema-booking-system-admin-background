# Author: wy
# Time: 2022/12/10 17:48
import re


class CommonPattern:
    numberPattern = re.compile(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$')
    sexPattern = re.compile(r'^男|女$')
    usernamePattern = re.compile(r'^\w{3,20}$')
    passwordPattern = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,30}$')
    moneyPattern = re.compile(r'^(0|[1-9]){1,5}(\.[0-9]{1,2})?$')
    codePattern = re.compile(r'^[A-Za-z]{5}$')
    birthPattern = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}')
    @staticmethod
    def confirm(pattern, input_str):
        return re.match(pattern, input_str) is not None


if __name__ == '__main__':
    input_str = "a"
    res = CommonPattern.confirm(CommonPattern.usernamePattern, input_str)
    print(res)
