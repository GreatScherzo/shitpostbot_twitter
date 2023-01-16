# shitpostbot_twitter
 A bot made to post shitpost on twitter. Made using Python.
The bot randomsly select a *template image* and an *insert image*, crops the *insert image* and paste it onto the *template image*, and post it on twitter.

# Usage

### Run from source
To run the bot from source code, execute main.py.

### Run from EXE file
There\`s also an EXE file if you wish to avoid installing all the necessary python packages. Just run the EXE file with the res folder in the same directory.

```
└── project folder
    ├── shitpostbot.exe
    ├── res
    │   └──  ....
    └── ...
```
After running the exe file, type in `run` in the command prompt to execute the bot.

### Twitter Key
To enable the bot to post to twitter, you need to have a twitter dev account and acquire your own security credentials for your twitter app (consumer key, consumer secret, access token, access secret).

Input the your credentials into the twitter_key.csv as below.

```
consumer_key, (insert required info here)
consumer_secret, (insert required info here)
access_token, (insert required info here)
access_secret, (insert required info here)
```

### Resources Required
The bot needs *template images* and *insert images* to generate a shitpost.
Furthermore, *template images* needs to have a mask for the bot to know where to paste the insert image.
Example are as below.

*template images* and *insert images* need to be \`registered\` in template_info csv.
Example is as below.
```
name,num_of_inserts,is_background_insert,enable_alpha_insert,must_use_label,label
WhichSideOn,2,1,1,0,neutral,high,0,neutral
```
### Template_info.csv Settings
You can set detailed parameters using the template_info.csv

| Parameter  |  Explanation |
| ------------ | ------------ |
|  name | Name of template image to be registered. Mask of the template image must have the same name with "_mask" attached behind its name.|
|  num_of_inserts | Number of insert images the template accepts.   |
|  is_background_insert  | Sets if the background of the template is to be inserted an image (doesnt seem to affect the result tho, to be further improved in the future)  |
|  enable_alpha_insert |  Sets if alpha channel is added when inserting image for transparency effect  |
|  must_use_label | If true, forces the bot to use only insert images in said label in label parameter  |
|  label | label of insert images that must be used when must_use_label is true. Multiple labels can be set.  |

#### Res Folder Structure
*template images*, *insert images*, *masks*, and template info csv are kept in res folder.
The structure of res folder is as below.

```
└── res
    ├── insert_image
    │    ├── [label_1]
	│	│	└── insert1.jpg
	│	├── [label 2]
	|	|	└── insert2.jpg, insert3.jpg, ...
	│	└── ...
    ├── mask
	│	└── insert1_mask.bmp, 
	│	　　　insert2_mask.bmp,　...
	├── template_image
	│	└── template1.jpg, template2.jpg, ...
	└── template_info.csv
```
# Inquiry
If you need help at somewhere or have suggestions, feel free to sumbit an issue!


