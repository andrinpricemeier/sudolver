from typing import Optional
import boto3


class ImageAnalysis:
    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_region: Optional[str] = None,
    ) -> None:
        self.client = boto3.client(
            "textract",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )

    def analyze(self, image_bytes):
        return self.client.analyze_document(
            Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
        )
