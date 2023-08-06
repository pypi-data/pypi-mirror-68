from pydantic import BaseModel


class Usage(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                'cur_rate': 0,
                'rate_limit': 30,
                'month_requests': 93,
                'monthly_limit': 300
            }
        }


class Login(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGJinz18ji2IUzI1NiJ9"
                                ".eyJzdWIiOiJhcm5hdWQuaGVuKO92jiAklwaXRhLmZyIiwiZXhwIjoxNTg2MDMxNjc4LCJhZG1pbiI6dHJ1ZX0"
                                ".KrbkD8RYZDbxkoszi1DLZbHBvzsZg_X91Huhdf1LdtrdkAXY",
                "token_type": "bearer",
                "expiration": "2020-04-04T20:21:18.347056"
            }
        }
