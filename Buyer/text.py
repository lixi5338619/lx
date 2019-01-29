from alipay import AliPay

def Pay(order_id,money):
    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6sQOnniaLJXnCkB48tbPOXP98KKiGGzOnixCeLxUdgGtZcZ49UKdYml4j9Kx4brg1ZyVm4eJ4nunTFJZp11xf0mMX9HPRMHGvgadj0Vhi/4gYw7r20MZd/hU1IxvTqvFsyuSsuvofe1xZf4YeOI3xidKQ1DYkbYNKVARfMKc2rzoW0iYpBR96xKna/Ye1eP70dPY1SqY2wFwUWU93uMc8FfzUjxmOtiJY8JSRo3bsLYWj96u1ivpe1DuyXNbcTvygo0p9EuSCtq8cUBOj1eTJm/L4d0xT7xef9n+3ZER156QCgjeMAB7pnkIHF2yySVSmVoR2VL9umYdMAZ/jsJe2QIDAQAB
    -----END PUBLIC KEY-----'''

    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEpQIBAAKCAQEA6sQOnniaLJXnCkB48tbPOXP98KKiGGzOnixCeLxUdgGtZcZ49UKdYml4j9Kx4brg1ZyVm4eJ4nunTFJZp11xf0mMX9HPRMHGvgadj0Vhi/4gYw7r20MZd/hU1IxvTqvFsyuSsuvofe1xZf4YeOI3xidKQ1DYkbYNKVARfMKc2rzoW0iYpBR96xKna/Ye1eP70dPY1SqY2wFwUWU93uMc8FfzUjxmOtiJY8JSRo3bsLYWj96u1ivpe1DuyXNbcTvygo0p9EuSCtq8cUBOj1eTJm/L4d0xT7xef9n+3ZER156QCgjeMAB7pnkIHF2yySVSmVoR2VL9umYdMAZ/jsJe2QIDAQABAoIBAQDRz/SsxmYrkLESpXoyta4vz61VAVRS9fNWw4GIu+/UIz2f5tg1gZp82HwqNYhKkCTeY/oFLQYbBp4HBNYhUM7djpLJFA7kiTYgoHLyF3TNk4nIXg6GQBqj8KmH6BaWPcgLj9ak11dKLAobuBKQ/sQP8Q9ayAc1enmawXdPg/KBPXtHbU1fOYVKiDhCXLfkAMBZck7b1m1BU7KSS32zToOxFYqHV3sj2YsnqiUXaip5SoHmEqIQkmKoJ684HD8u//1ttXh9SZxUGFVF6OJyRAA7yGXm0tM4yt5Oiv449IlhfTEAP6smrAzY7diETG/YqHfTM+WojnMoQoC5qGwzhdwNAoGBAPe0oc/g2+MkaMHX37sdAXqmMap4DlK/dIEKy9CD/NzU2RL9YbXiA8TNgupu1nOkuc9C8S5CHfGrspDWOjdktTwtA6va6urGVfC02fbUzfzrCLzVtZTFmhn/RXWpww3ogv24mhDt/acln384G6FMCR9hiKSJQuBKOANwfgYAVyF7AoGBAPKggPBMV1eIFu5HMnP+60nL3yAuEREavN6JKVJL63yR5yfZzLscWZG11pdnIPlWdp6m7H8S6xsVx++JaMtBe0xdxIXzOGi5Ksqdr4wLybnCMJZbSwBY/1GK9r5glrFxyWLNNb1eXz9j85vXttUnfogJ3Fdmbpp5UiIauD5XaZ67AoGAHhzAWwQL1xYTAhWbJiUFjAJuIToNC7QolpNYaZXSBIp/hRZ2bWT3blJJavRkb5SD3hVWOnhhKYLk50STuS4t9g3G13p6emX4BpYFtULzc56i5knYlChdbnGg4QftJWCxo+RwHkTARDSHqjCI81fJ+B2kPdRN4/RB0PE48MPT08cCgYEAr7E8TUXqxW69tCQIS+jftpuT4jiZkTo8ZCUMsBRb3OPGcJwN3byEu7fiQdajEQrkcLRNcyNe7kkSc8mcAftT7pPD+H+MbIERlJElCpOKqyIMjwRixkir8f9f97H3zVypSQtyi8Nn035sbICDW8zymk4RqZR6KRALQrj4i+Q+jnsCgYEAliH3B06QG7ToxLx2YRKDkUPo/BS/kgJZsjfZMAOp6z8mpCiC4NoB7l8V4djBmENMK3M4/S0eLYnBiAlPa5GOGfTCfPqP9CncGlkaF6TTS0lzUJm7qcBydP59sUprJXJBtTyYUvmaRnXm8t/fdFJKndY//Ot3P+cLWDyP/2iQ7ZQ=
    -----END RSA PRIVATE KEY-----'''

    alipay = AliPay(
        appid="2016092400585696",  # 支付宝app的id
        app_notify_url=None,  # 会掉视图
        app_private_key_string=app_private_key_string,  # 私钥字符
        alipay_public_key_string=alipay_public_key_string,  # 公钥字符
        sign_type="RSA2",  # 加密方法
    )
    # 发起支付
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(money),  # 将Decimal类型转换为字符串交给支付宝
        subject="全球生鲜",
        return_url="127.0.0.1:8000/callbackPay/", #完成之后返回
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 让用户进行支付的支付宝页面网址
    return "https://openapi.alipaydev.com/gateway.do?" + order_string
