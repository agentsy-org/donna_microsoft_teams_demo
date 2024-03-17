#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from dotenv import load_dotenv
load_dotenv(override=True)

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    print(APP_ID)
    print(APP_PASSWORD)
    # APP_ID = "21f451a3-a1c3-4e0f-afca-6009904ffb44"
    # APP_PASSWORD = "K~w8Q~V8kYbJqutw625cjdTsUbArWm_zyMqqAcnx"