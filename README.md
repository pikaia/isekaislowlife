# isekaislowlife
Isekai slow life Python bot

# Bluestacks
## Settings 
### display resolution
#### Landscape
#### 1600 x 900
### Mouse cursor style
#### Bluestacks

# pyautogui
## Tweak confidence higher when image doesnt match. A sign is if it thinks its matching wrongly.

# Isekai slow life game data.
In each building in the village, there is a detailed breakdown of how a building gets its earnings. 

## Fellow Operation Ability
This is the total power of all your fellows. Eg you can see it in the Fellow tab:

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/306b2124-656d-43db-95e2-c8c754f64e57)

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/e929804d-7029-49e9-87c9-98603b223b40)


## Total Employee Earnings
This is Employee Earnings rate x the number of employers eg 1 x 8022 = 8.022 K/s
![image](https://github.com/pikaia/isekaislowlife/assets/1948869/78c6150c-cfe8-476d-930d-e92dc0419b51)

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/38bbe592-3fea-484e-be4d-57a87d187965)

Basic Earnings is the total of Fellow, total employee, fish adjusted to k/s.

## Fish

This is the number of employees multiplied by the fishing bonus for building earnings.

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/dd76fa33-c9bb-4001-93e3-fb74e194ddc1)

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/027207bd-8a25-46ce-9310-7a5ea813f885)

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/52838791-441b-46be-b9b3-5fee1e5c747b)

eg 28325/s = 5665 * 5

The extra buff for unfettered comes from the Combination Enclyclopedia, The bubbble family.

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/d73e3806-cc73-4b61-a82f-c91ca71be2ea)

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/095d6268-043c-493d-8d52-38935e299d44)



## Operating Fellow
The Operating Fellow is the sum of each fellow assigned to building.

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/fd15202c-3884-4919-ba05-617d4fadfa07)

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/b6f35f9b-f31b-4ef2-ab91-c33b9c7f31d8)

So in this particular example, its 295%+225%+295%+230% = 1,045%


## Upgrade
This corresponds to the buildings level. The figures are obtained by observation. They are not listed in  the same. From looking at current game state, we can guess the numbers are:

| Level	| Upgrade |
| ----- | ------- |
| 5	    | 700%   |
| 6	    | 1100%  |
| 7	    | 1400%  |
| 8	    | 1900%  |


# Family Member

The Family Member refers to the class score for the building class. This looks up the table in the Home screen, family, family bonus:

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/53a4f3c6-c81c-4223-a12b-d6f728c54aa0)

eg the Apothecary is an Informed class, so its value is 4717%

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/14d7828d-e4fb-4baf-b3cc-3876c87901c7)

## Farmstead

Farmstead bonus comes straight from farmstead:

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/c7f6eed2-2436-4645-8570-fe17aeb0ec2b)


## Inn
This is the contribution from developing the Inn's menu.

This screenshot shows the Inn is taken from the numbers in the Inn, Menu screen.
eg the Scroll Shop is an Inspiring type building, so its bonus is 945%

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/6643f11f-2fa4-4e72-8e5c-e3cd7f4d830a)

# 20240607 Treasure Inn update
With this update another variable is added to the building earnings.

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/0c91f63e-e572-4300-ae1a-ed2fabc0416b)

There are 10 treasures that give different buffs. In particular, there is a buff for each building type.

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/8f8eaa78-cd58-4156-8f3e-e815b8c8c992)

The first treasure Inn number comes from the basic earnings buff.

In this screenshot it is +14, and the number of empoyees was 9667. 14*9667 = 135338 or 135.3 K/s

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/e30a3cd9-390e-456b-a739-04d612bf5295)

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/31bc4391-5f68-42f7-82a2-577738370b7e)


The individual buff gives the Treasure Inn bonus. Add the Treasure Inn bonus to the earnings bonus to derive the total earnings bonus.

## Magic farm
This seems related to the plant encylopedia totals and the earnings increase from the money tree.

eg for the scroll shopt, an Inspiring building, its 600+200 = 800

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/c103f373-a852-4d97-8e39-914b112ba830)

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/0415507e-4707-41ea-8f5d-6b979d675ba2)

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/6b80af1a-1e52-4f38-8487-d656b4942bb8)


## Fish

The fishing bonus can be seen in the fishing bonus screen beneath the fishing encyclopedia. Its a simple number without any variation for all buildings.

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/65423483-e71a-4467-bb3e-00e598b9c60a)

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/7026468c-7ca5-4fc9-ad1f-a6b31cb5e662)


## Challenge

This comes from the current level in the Challenge tower.

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/5d0c3b54-f485-488d-918c-3362bf940237)

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/e0954f52-de38-4e1d-a984-95ddcad208da)


## Guild

Guild numbers are available under Guild, head office. It reflects the total deployed fellows for each building class eg Inspiring:

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/6da67894-4b17-49a8-856e-395be6f2035d)

![image](https://github.com/pikaia/isekaislowlife/assets/1948869/9d5dea52-35e4-4751-85f0-be251f8f5135)


