# url for this code:

https://github.com/pleabargain/idioms_CRUD


current status: 
Fixing what I broke!


# goal(s) 

create a CRUD app that allows users to select and import the JSON file to sqlite
and allows user to perform CRUD operations in an HTML interface


And now that the app mostly works I can see that I can keep adding features and etc.

I'm going to move on now.

# problem
I don't know how (yet) to add an additional context to an existing phrase. I didn't think through my database requirements very well and now I have a problem of how to add more nuances. 

```
{"idioms": 
    [
        {"phrase": "Rub It In: Teasing someone to make them feel even worse after a defeat.", 
        
        "context": ["Alright you beat me. But there\u2019s no need to rub it in."]}
    ,

    ]

}

```

It should have been more like

```
Idioms
    phrase
        context
        *
    category

```

I wanted context to be an array of items with multiple entries connected to it.

Live and learn right?


# soft requirements

I used github copilot a lot! And I mean a lot!


# some mechanics

```

pipreqs --encoding utf-8 "./"


```



---
* js goes inside the BODY tag! doh!

* as soon as I wanted to demonstrate the app, it failed! OFC!

* lots of debugging to get the app started. 

* chatgit hubpilot doesn't wirte the best code out of the box.

* Flask secret key was a real pain

* Made huge progress over the course of 90 non-sequential minutes.

* Initially it was very much an ETL process!

# to do
* verify edit.html writes to the DB
* Clean up the UI
* * confirm to user that a new item has been added
* add user log in and authorization

# Done
done: convert text to json
done: having trouble getting the database created!
done: added more error correction
done: added a basic CSS
