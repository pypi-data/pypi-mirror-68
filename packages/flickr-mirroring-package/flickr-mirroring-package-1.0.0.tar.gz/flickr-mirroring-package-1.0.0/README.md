# WHAT THE PROJECT DOES ?
Package flickr-mirroring-package use to batch download photos from user Flickr

# WHY THE PROJECT IS USEFUL ?
- It does not take much time instead manual download

# HOW TO USE ?
- Open Terminal
- pip install flickr-mirroring-package

# USAGE ?
## Donload Photo
- Download photos according to the specified caching strategy FIFO or LIFO

- For example:
$ ./flickr.py --username manhhai --lifo
2020-03-23 08:49:27,630 [INFO] Scanning page 1/1026...
2020-03-23 08:43:40,648 [INFO] Caching image of photo 6dbf9c52ccec1722e32161cd41d6a290...
2020-03-23 08:43:41,546 [INFO] Caching image of photo f5275b3940b714fdb083995086ca2b83...
2020-03-23 08:49:27,660 [INFO] Caching image of photo ee6557cf53ebcfdbd66c617ca9e6c75f...
2020-03-23 08:49:32,540 [INFO] Caching image of photo 0e35aa2fab6527ebc98cc7a285d2cc12...
2020-03-23 08:49:33,637 [INFO] Caching image of photo 397d6bc91f7f6642373a5323dea291fb...


$ ./flickr.py --username manhhai --fifo
2020-03-23 10:34:45,467 [INFO] Scanning page 1026/1026...
2020-03-23 10:34:45,467 [INFO] Caching image of photo ba892a4943e1c1dd07379f92068eac7e...
2020-03-23 10:34:46,821 [INFO] Caching image of photo efd816c67a2bbd8eb47559c2a98b0320...
2020-03-23 10:34:47,680 [INFO] Caching image of photo 134d76e411acef10089b17e532b7245f...
2020-03-23 10:34:48,907 [INFO] Caching image of photo a38c7c8156c8fbe309d354f750c4880d...
2020-03-23 10:34:50,100 [INFO] Caching image of photo e8ad574c0f4733fc116c6f1c9cb92035...

- Use --info-only: Fetch info only.
    + 0: (default): The title of the photo only.
    + 1: The title and the description of the photo.
    + 2: The title, the description, and the textual content of the comments of the photo.

- For example:
$ ./flickr.py --username manhhai --save-api-keys --fifo --info-only --info-level 2
2020-03-23 12:16:30,560 [INFO] Scanning page 1026/1026...
2020-03-23 12:16:32,919 [INFO] Caching information of photo 576b89d947576c3cb6c72cbbf7e3107a...

$ ./flickr.py --username manhhai --save-api-keys --fifo --info-only --info-level 2
2020-03-23 12:16:30,560 [INFO] Scanning page 1026/1026...
2020-03-23 12:16:32,919 [INFO] Caching information of photo 576b89d947576c3cb6c72cbbf7e3107a...

$ cat ~/.flickr/manhhai/5/7/6/b/576b89d947576c3cb6c72cbbf7e3107a.json | json_pp
```{
   "title" : {
      "content" : "Đoàn công tác SV ĐH Kiến Trúc Sài Gòn tại Côn Đảo, tháng 3-1976",
      "locale" : "vie"
   },
   "description" : {
      "locale" : "eng",
      "content" : ""
   },
   "comments" : [
      {
         "locale" : "vie",
         "content" : "Hi, Manh Hai nhung ngay ong miet mai o DHKT toi o CDSP bay gio toi dau dau voi nhung ban ve nha va co so thuong mai con ong thi sao. Co la Civil Engineer o hai ngoai?"
      },
      {
         "content" : "Dear PhamOrama:Cám ơn bạn đã hỏi thăm, tôi vẫn sống ở VN từ 1975.",
         "locale" : "vie"
      },
      {
         "content" : "Internet ngon nhieu gio cua toi, nen thu that hom nay moi re-install. Manh Hai post tam anh &quot;so cute&quot;. Con nit ben nay khon lanh hon tuoi nho cua chung ta nhieu lam. Co ut Tami Pham cua toi moi len 7 va hoc lop 2 ma gioi nhu tuoi toi luc lop5. Chuc Ban va gia dinh mot nam moi an khang, thinh vuong.",
         "locale" : "vie"
      },
      {
         "locale" : "eng",
         "content" : "[https://www.flickr.com/photos/13476480@N07/1718051545/in/photostream/]"
      }
   ]
}
```

# CONTACT 
- Email: khoi.vo@f4.intek.edu.vn
- Github : https://github.com/intek-training-jsc/sprite-sheet-KV16
