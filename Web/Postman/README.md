# Postman


**Category:** Web

**Points:** 100

**Description:**

Hey, some kaсkers steal my mail. Can you help return and deliver it?

tasks.open.kksctf.ru:8001

@greg0r0

## WriteUp

First, check robots.txt and see /postbox route

Solve is simple (hint in title of task):
```
curl tasks.open.kksctf.ru:8001/postbox -XPOST
```
**Flag:** kks{thanks_f0r_m@1l}
