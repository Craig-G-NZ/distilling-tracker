# distilling-tracker

This is a flask website used to track my distillations. From ingredients, fermentation, specific gravity, through to the end product. It's storing information that I want to store in the database. I am not sure how much development I will be doing, but if you post an issue I might be able to help out.

To use.....

    docker run -d \
      --name distilling-tracker \
      --restart always \
      -p 80:80 \
      -v /data_dir:/app/data:z \ #optional
      -e TZ=Pacific/Auckland \
      skippynz/distilling-tracker:latest

Optional: Create a directory: and name it whatever you want e.g. data_dir - this will be used above in your docker command for the volume (-v). An empty database will be automatically created in the "data_dir" folder. If you want change the name and title of the website, you will need to create a config.json file in the data_dir folder with the following content. Change as you see fit. If you dont create the file it might self name to "Default Title" and "Default Name".

    {
    "website_title": "Distilling Tracker",
    "website_name": "Distilling Tracker"
    }   

Feel free to create an issue if you want to discuss anything.

![image](https://github.com/Craig-G-NZ/distilling-tracker/assets/92700720/1e949236-d38e-417e-af1c-b4397548f546)
![image](https://github.com/Craig-G-NZ/distilling-tracker/assets/92700720/af3cb8b0-e110-4fc4-8e27-13853df857bb)
