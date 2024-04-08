# Gravis
> **Project in development, more documentation and code to be added**

![gravis_chassis_render_occlusion (1)](https://github.com/42dotmk/Gravis/assets/30288047/844e40d8-6557-4429-ae0f-7ff86c949bb5)

## Introduction (project still in development)
Gravis is an open-source robot with the aim to make replicating it an easy and fun process, so that anyone who is interested in robotics can get into the field and progress. Parts of Gravis are 3D printable, except for the chassis which is premade (link for it will be provided). The electronics are all readily available and relatively cheap such as the Raspberry Pi, Jetson Nano and other Arduino modules which make upgrading and repairing him an easy process. This document will contain a guide on all of the parts and how they are connected, so that you can easily start making your own Gravis. The README file shall be updated consistently with new changes and it is the documentation for the entire project.

## Project roadmap
The project is still being planned so I will post updates on it regularly. The end goal is to have everything open-source, including the 3d printable parts. Soon there will be ML models on this github repository that will utilize Gravis' camera.
  ### Links for social media related to this project ###
  - [The Making Robots Subreddit](https://www.reddit.com/r/makingrobots/)
  - [Github repository for the Ricardo robot](https://github.com/dimitarbez/Ricardo)

## Part list
  > **The product links are the places where I ordered the parts from**
  - Raspberry Pi 4 2GB
  - Arduino Mega R3 2560
  - 3S LiPo
  - DC5V WS2812B Individually Addressable 5050 RGB Led Strip | [Product link](https://www.aliexpress.com/item/32682015405.html?spm=a2g0o.order_list.order_list_main.151.3b271802y7MnsQ)
  - Stepdown voltage converter 12V-5V [Product link](https://www.aliexpress.com/item/33037061522.html?spm=a2g0o.order_list.order_list_main.146.3b271802y7MnsQ)
  - DHT22 Temperature sensor | [Product link](https://www.aliexpress.com/item/33037061522.html?spm=a2g0o.order_list.order_list_main.146.3b271802y7MnsQ)
  - 2x AIYIMA 40MM Mini Speakers | [Product lin](https://www.aliexpress.com/item/32836767822.html?spm=a2g0o.order_list.order_list_main.141.3b271802y7MnsQ#nav-specification)
  - TS400 Robot chassis | [Product link](https://www.aliexpress.com/item/32966785172.html?spm=a2g0o.9042311.0.0.27424c4do5r4TH)
  - Slamtec RPLidar A1M8R6 | [Product link](https://www.dfrobot.com/product-1125.html)
  - 2x L298N Motor controller | [Product link](https://www.aliexpress.com/item/33012645746.html?spm=a2g0o.9042311.0.0.27424c4dGmtTvO)
  - MPU6050 Accelerometer and Gyroscope | [Product link](https://www.aliexpress.com/item/32340949017.html?spm=a2g0o.productlist.0.0.a95832a5qxBww1&algo_pvid=981da1eb-5f62-4149-9e9a-a396d7ae606d&algo_exp_id=981da1eb-5f62-4149-9e9a-a396d7ae606d-0&pdp_ext_f=%7B%22sku_id%22%3A%2210000000609322940%22%7D&pdp_pi=-1%3B1.16%3B-1%3B-1%40salePrice%3BUSD%3Bsearch-mainSearch)
  - 10W+10W PAM8610 D Class Dual-channel HIFI Audio Amplifier Board | [Product link](https://www.aliexpress.com/item/32612268830.html?spm=a2g0o.order_list.order_list_main.116.3b271802y7MnsQ)
  - 2x 9g Servo motor (for the camera holder) | [Product link](https://www.aliexpress.com/item/4000903734519.html?spm=a2g0o.productlist.0.0.421a5deaZENHVL&algo_pvid=67ecde94-4cdf-4ab3-bc57-f7a76f9d21d8&algo_exp_id=67ecde94-4cdf-4ab3-bc57-f7a76f9d21d8-1&pdp_ext_f=%7B%22sku_id%22%3A%2212000021325362154%22%7D&pdp_pi=-1%3B5.19%3B-1%3B-1%40salePrice%3BUSD%3Bsearch-mainSearch)
  - Raspberry Pi Camera v1.3 | [Product link](https://www.aliexpress.com/item/32988983058.html?spm=a2g0o.productlist.0.0.d2c6601dINeh3L&algo_pvid=2dc3068e-94cb-4ead-babf-3f1e0dea7f04&algo_exp_id=2dc3068e-94cb-4ead-babf-3f1e0dea7f04-0&pdp_ext_f=%7B%22sku_id%22%3A%2266896320728%22%7D&pdp_pi=-1%3B4.15%3B-1%3B-1%40salePrice%3BUSD%3Bsearch-mainSearch)
