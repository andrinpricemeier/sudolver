export class ImageBase64 {
  constructor(private readonly imageBase64: string) {}

  getDataImageBase64() {
    return this.imageBase64;
  }

  getImageBase64(): string {
    return this.imageBase64.replace("data:image/jpeg;base64,", "");
  }
}
