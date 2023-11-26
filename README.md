# distilling-tracker

This is a flask website used to track my distillations. From ingredients, fermentation, specific gravity, through to the end product. It's storing information that I want to store in the database. I am not sure how much development I will be doing, but if you post an issue I might be able to help out.

To use.....

  docker run -d \\ \
    --name distilling-tracker \\ \
    --restart always \\ \
    -p 80:80 \\ \
    -v /data_dir:/app/data:z \\ \
    -e TZ=Pacific/Auckland \\ \
    skippynz/distilling-tracker:latest

Create one directory: data

An empty database will automatically be created in the data folder.

Feel free to create an issue if you want to discuss anything.
