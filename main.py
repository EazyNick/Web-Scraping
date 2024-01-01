import requests
from bs4 import BeautifulSoup
import os

# 이미지를 다운로드하는 함수
def download_image(image_url, folder_name="images"):
    if not os.path.isdir(folder_name):  # 이미지 저장 폴더가 없으면 생성
        os.makedirs(folder_name)
    
    response = requests.get(image_url)  # 이미지 URL로 요청 보내기
    if response.status_code == 200:     # 요청이 성공하면,
        # URL에서 파일 이름 추출
        image_name = os.path.join(folder_name, image_url.split("/")[-1])
        with open(image_name, 'wb') as file:
            file.write(response.content)  # 이미지 파일 쓰기
        print(f"Downloaded {image_name}")
    else:
        print("Failed to retrieve image", response.status_code)

# 웹 페이지에서 이미지 URL을 찾는 함수
def find_images(url):
    response = requests.get(url)
    if response.status_code != 200:
        print('Failed to retrieve the webpage')
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')  # 모든 이미지 태그 찾기
    image_urls = [img.get('src') for img in images]  # 이미지 URL 리스트 생성
    return image_urls

# 메인 코드
def main():
    url = input("Enter the URL of the site you want to scrape images from: ")
    image_urls = find_images(url)  # 이미지 URL 찾기

    if image_urls:
        print(f"Found {len(image_urls)} images.")
        # 각 이미지마다 다운로드
        for image_url in image_urls:
            download_image(image_url)
    else:
        print("No images found.")

if __name__ == "__main__":
    main()
