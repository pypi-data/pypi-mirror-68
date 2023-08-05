# Flickr Mirroring

![Flickr Home Page](flickr_homepage.png)

[Flickr](https://www.flickr.com/) is certainly the most popular photo-sharing platform and social network where users upload photos for others to see. Users create a free account and upload their own photos to share with friends and followers online. Flickr has more than ten million registered members worldwide. Between 3 and 4 million new images are uploaded daily.

## Photostream

**Photostream** is the most notable Flickr feature. The photostream of a user corresponds to the feed of their public photos. Any uploads the user sets to be publicly viewable will appear in this section.

When a user uploads a photo to Flickr, they can add:

- A **title**
- A **description**, to tell viewers what the photo is about,where it was taken, or any other details that matter.
- **tags**, to increase the chances of the photo showing up in search results.

Users can leave **comments** on a photo, to say what they like about this photo, or even ask a question to encourage a reply from the owner. Most of the time, the most valuable information about a photo lies in the comments posted by users.

Also, when uploading a new image, Flickr generates multiple resolutions of the original image:

- Square (75 x 75, 150 x 150)
- Thumbnail (100 x ...)
- Small (240 x ..., 320 x ...)
- Medium (500 x ..., 640 x ..., 800 x ...)
- Large 1024 (1024 x ..., 1600 x ..., 2048 x ...)

Of course, photographers always retain full control over which sizes of their images are available for viewing.

## The Commons Project

Old photos are one of the most important [historical sources](https://www.hist.cam.ac.uk/prospective-undergrads/virtual-classroom/historical-sources-what) for historical research and conservation projects. They provide us information about history at the most basic level. They are often used to build up a narrative of past events.

However, finding old photos for a particular region of the world, and for a given period of time, is not an easy task as photos come from various collections disseminated on many websites.

Since January 2008, Flickr has run [The Commons project](https://www.flickr.com/commons/institutions/), with the goal of sharing hidden treasures from the world's public photography archives. The project’s first partner was [The Library of Congress](https://www.flickr.com/photos/library_of_congress/). On a list of participating institutions there are also [The British Library](https://www.flickr.com/photos/britishlibrary/) and [The Internet Archive Book Images](https://www.flickr.com/photos/internetarchivebookimages/), who are the largest contributors to the project so far. Each one offers more than 1 million photos, and counting.

![](34326265565_434f2bf3b9_o.jpg)
_(La Vang church, Quang Tri, July 6, 1972, Michel Laurent/AP)_

Some of the major Flickr photostreams are constantly updated with new photos uploaded almost every day. We would like to write a command-line script that mirrors a complete photostream, and that keeps the local mirror updated as soon as the photostream has new photos.

## Flickr API

Flickr supports an [Application Programming Interface (API)](https://www.youtube.com/watch?v=GZvSYJDk-us) that [allows developers](https://www.smashingmagazine.com/2018/01/understanding-using-rest-api/) to [access Flickr data](https://www.flickr.com/services/api/).

To be able to use the [Flickr REST API](https://www.flickr.com/services/api/request.rest.html), you need to create a Flickr account and [register your application](https://www.flickr.com/services/api/keys/apply/) to Flickr to get API keys (consumer key and consumer secret).

Let's try the Flickr API with an amazing [photostream with over 100,000 historical images of Vietnam](https://www.flickr.com/photos/13476480@N07) taken between 1865 and 1975. We will use the first method [`flickr.people.getPhotos`](https://www.flickr.com/services/api/flickr.people.getPhotos.html) with the following arguments:

- `api_key`: Enter your API key
- `user_id`: `13476480@N07`
- `per_page`: `5`
- Output: `JSON`
- Do not sign call: Checked

Click on the button `Call Method...`. You will obtain a result in which the structure is similar to the following (the data may differ):

```json
{
  "photos": {
    "perpage": 5,
    "page": 1,
    "total": "101311",
    "pages": 20263,
    "photo": [
      {
        "farm": 66,
        "id": "49499525286",
        "ispublic": 1,
        "isfamily": 0,
        "isfriend": 0,
        "secret": "e6f0b9d940",
        "owner": "13476480@N07",
        "title": "SAIGON 1938 - Nhà rồng (trụ sở hãng vận tải biển Messageries Maritimes tại Saigon)",
        "server": "65535"
      },
      {
        "owner": "13476480@N07",
        "title": "SAIGON 1938 - Nhà rồng (trụ sở hãng vận tải biển Messageries Maritimes tại Saigon)",
        "server": "65535",
        "secret": "c629a2f8ca",
        "isfriend": 0,
        "id": "49499522706",
        "ispublic": 1,
        "isfamily": 0,
        "farm": 66
      },
      {
        "secret": "475b4e6626",
        "isfriend": 0,
        "title": "HẢI PHÒNG 1938 - Trụ sở hãng vận tải biển Messageries Maritimes tại Hải Phòng",
        "owner": "13476480@N07",
        "server": "65535",
        "farm": 66,
        "ispublic": 1,
        "id": "49499024083",
        "isfamily": 0
      },
      {
        "secret": "8d6cbec749",
        "isfriend": 0,
        "title": "HANOI 1973 - Góc Phố Đinh Tiên Hoàng-Hàng Khay",
        "owner": "13476480@N07",
        "server": "65535",
        "farm": 66,
        "ispublic": 1,
        "id": "49496075888",
        "isfamily": 0
      },
      {
        "isfriend": 0,
        "secret": "4e4b382a0c",
        "server": "65535",
        "title": "HANOI 1973 - Cửa hàng Bách hóa Tổng hợp, góc Phố Tràng Tiền & Phố Hàng Bài",
        "owner": "13476480@N07",
        "farm": 66,
        "isfamily": 0,
        "ispublic": 1,
        "id": "49496564661"
      }
    ]
  },
  "stat": "ok"
}
```

This data corresponds to the _most recent photos_ (at the time this mission was written, indeed) published by PHẠM Mạnh Hải on [his Flickr photostream](https://www.flickr.com/photos/13476480@N07/):

![](flickr_api_search_photos_manhhai.png)

This request corresponds to the following URL:

```text
https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=<<your-api-key>>&user_id=13476480%40N07&per_page=5&format=json&nojsoncallback=1
```

_Note: Replace `<<your-api-key>>` with your API key._

You can use the command line tool [cURL](https://curl.haxx.se/docs/httpscripting.html) to send this HTTP request to Flickr server and get the result:

```bash
$ curl -XGET "https://www.flickr.com/services/rest/?method=flickr.people.getPhotos&api_key=<<your-api-key>>&user_id=13476480%40N07&per_page=5&format=json&nojsoncallback=1"

{"photos":{"page":1,"pages":20263,"perpage":5,"total":"101311","photo":[{"id":"49499525286","owner":"13476480@N07","secret":"e6f0b9d940","server":"65535","farm":66,"title":"SAIGON 1938 - Nh\u00e0 r\u1ed3ng (tr\u1ee5 s\u1edf h\u00e3ng v\u1eadn t\u1ea3i bi\u1ec3n Messageries Maritimes t\u1ea1i Saigon)","ispublic":1,"isfriend":0,"isfamily":0},{"id":"49499522706","owner":"13476480@N07","secret":"c629a2f8ca","server":"65535","farm":66,"title":"SAIGON 1938 - Nh\u00e0 r\u1ed3ng (tr\u1ee5 s\u1edf h\u00e3ng v\u1eadn t\u1ea3i bi\u1ec3n Messageries Maritimes t\u1ea1i Saigon)","ispublic":1,"isfriend":0,"isfamily":0},{"id":"49499024083","owner":"13476480@N07","secret":"475b4e6626","server":"65535","farm":66,"title":"H\u1ea2I PH\u00d2NG 1938 - Tr\u1ee5 s\u1edf h\u00e3ng v\u1eadn t\u1ea3i bi\u1ec3n Messageries Maritimes t\u1ea1i H\u1ea3i Ph\u00f2ng","ispublic":1,"isfriend":0,"isfamily":0},{"id":"49496075888","owner":"13476480@N07","secret":"8d6cbec749","server":"65535","farm":66,"title":"HANOI 1973 - G\u00f3c Ph\u1ed1 \u0110inh Ti\u00ean Ho\u00e0ng-H\u00e0ng Khay","ispublic":1,"isfriend":0,"isfamily":0},{"id":"49496564661","owner":"13476480@N07","secret":"4e4b382a0c","server":"65535","farm":66,"title":"HANOI 1973 - C\u1eeda h\u00e0ng B\u00e1ch h\u00f3a T\u1ed5ng h\u1ee3p, g\u00f3c Ph\u1ed1 Tr\u00e0ng Ti\u1ec1n & Ph\u1ed1 H\u00e0ng B\u00e0i","ispublic":1,"isfriend":0,"isfamily":0}]},"stat":"ok"}
```

You get the idea of how easy it is to use the Flickr API.

Your mission, should you choose to accept it, is to use the Flickr [REST API](https://www.youtube.com/watch?v=7YcW25PHnAA) to list all the public photos of a specified user, to download the image in the highest available resolution of each photo and the data of this photo (title, description, and comments).

@todo: describe the mission more completely 

https://en.wikipedia.org/wiki/Representational_state_transfer

# Fetching Information from Flickr API

## Waypoint 1: Flickr API Wrapper

As briefly presented, the Flickr API provides a set of [endpoints](https://en.wikipedia.org/wiki/Web_API#Endpoints) to fetch information about various resources (users, photos, comments, etc.).

We suggest that you use [Postman](https://www.youtube.com/watch?v=7E60ZttwIpY), an [API testing tool](https://en.wikipedia.org/wiki/API_testing), to [send requests](https://www.guru99.com/postman-tutorial.html) to the Flickr API server and to[get response](https://www.youtube.com/watch?v=uWrw0Bh7BVM) back.

We will start this mission by writing a little wrapper that will surface a few methods to fetch data from Flickr using its REST API. Write a class `FlickrApi` whose constructor takes two arguments `consumer_key` and `consumer_secret`, in this particular order. You can get a Flickr API non-commercial key by [applying online](https://www.flickr.com/services/apps/create/noncommercial/).

The class `FlickrApi` stores these API keys into private attributes of the built object.

For example:

```python
>>> flickr_api = FlickrApi('0123456789abcdef0123456789abcdef', '0123456789abcdef')
>>> flickr_api.consumer_key
AttributeError: 'FlickrApi' object has no attribute 'consumer_key'
```

## Waypoint 2: Flickr User

Flickr users are identified by a unique identification (NSID). When we need to fetch information from a user, such as the list of photos they have published on Flickr, we need to pass the identification of this user (not their username) to the request that we send to the Flickr API server. However, human beings remember usernames (e.g., `manhhai`) better than the identification of a user (e.g., `13476480@N07`). The Flickr API provides an endpoint to fetch the unique identification of a user by providing their username.

Write a class `FlickrUser` whose constructor takes two arguments `user_id` and `username`, in this particular order, where:

- `user_id` (string): Unique identification of a Flickr account (corresponding to the user's NSID).
- `username` (string): Username of this Flickr account.

Write two read-only properties `user_id` and `username` of the class `FlickrUser` that respectively returns the unique identification and the username stored in a `FlickrUser` object.

Example:

```python
>>> user = FlickrUser('39873962@N08', 'manhhai')
>>> user.user_id
'13476480@N07'
>>> user.username
'manhhai'
```

Add a static method `from_json` that takes an argument `payload` and returns an object `FlickrUser`. The argument `payload` corresponds to a JSON expression with the following structure (i.e., the information of a particular username as returned by the Flickr API method [`flickr.people.findByUsername`](https://www.flickr.com/services/api/flickr.people.findByUsername.html)):

```json
{
  "id": string,
  "nsid": string,
  "username": {
    "_content": string
  }
}
```

For example:

```python
>>> payload = {
  "id": "13476480@N07",
  "nsid": "13476480@N07",
  "username": {
    "_content": "manhhai"
  }
})
>>> user = FlickrUser.from_json(payload)
>>> user.user_id
'13476480@N07'
>>> user.username
'manhhai'
```

Add an instance method `find_user` to the class `FlickrApi` that takes one argument `username` (the username of a Flickr user) and that returns an object `FlickrUser`. The function sends a request to Flickr's API endpoint to [fetch the information about the user](https://www.flickr.com/services/api/flickr.people.findByUsername.html) specified by this `username`.

For example:

```python
>>> user = flickr_api.find_user('aleshurik')
>>> user.username
'aleshurik'
>>> user.user_id
'75571860@N06'
```

If Flickr servers raise an error, the method `find_user` MUST raise an object `Exception` with the returned error message. 

For example:

```python
>>> user = flickr_api.find_user('Elena Shumilova')
Exception: an error occurred
```

## Waypoint 3: Flickr Photo

Write a class `FlickrPhoto` whose constructor takes two arguments `photo_id` and `title`, and add a read-only property `id` that returns the identification of the photo.

_Note: We use the argument name `photo_id` instead of `id` because [`id` is a Python built-in](https://docs.python.org/3/library/functions.html#id). We should **NEVER** shadow Python built-ins. Another alternative is to name the variable with a single trailing underscore, such as `id_`, which is a [convention to avoid conflicts with Python keywords](https://www.python.org/dev/peps/pep-0008/#descriptive-naming-styles).\_

For example:

```python
>>> photo = FlickrPhoto('49510908217', "SAIGON 1974 - Rạch Bến Nghé, Bến Chương Dương")
>>> photo.id
'49510908217'
```

Add the static method `from_json` that takes an argument `payload` and returns an object `FlickrPhoto`. The argument `payload` corresponds to a JSON expression with the following structure (i.e., the information of a particular user as returned by the Flickr API method [`flickr.people.getPhotos`](https://www.flickr.com/services/api/flickr.people.getPhotos.html)):

```json
{
  "id": "49510908217",
  "owner": "13476480@N07",
  "secret": "6f78f65cfd",
  "server": "65535",
  "farm": 66,
  "title": "SAIGON 1974 - Rạch Bến Nghé, Bến Chương Dương",
  "ispublic": 1,
  "isfriend": 0,
  "isfamily": 0
}
```

For example:

```python
>>> payload = {
  "id": "49510908217",
  "owner": "13476480@N07",
  "secret": "6f78f65cfd",
  "server": "65535",
  "farm": 66,
  "title": "SAIGON 1974 - Rạch Bến Nghé, Bến Chương Dương",
  "ispublic": 1,
  "isfriend": 0,
  "isfamily": 0
}
>>> photo = FlickrPhoto.from_json(payload)
>>> photo.id
'49510908217'
```

## Waypoint 4: Localized Photo Title

We would like to identify the language used for the title of the photo, and to store this information along with the title. This can easily be accomplished with [Google's language-detection library](languagedetection-101203030754-phpapp01.pdf) that was [ported to Python](https://github.com/Mimino666/langdetect).

### Locale

A locale is a set of conventions for handling written language text and various units (i.e., date and time formats, currency used, and the decimal separator).

Conceptually, a locale identifies a specific user community - a group of users who have similar cultural and linguistic expectations for human-computer interaction (and the kinds of data they process). A locale’s identifier is a label for a given set of settings. For example, `en` (representing "English") is an identifier for a linguistic (and to some extent cultural) locale that includes (among others) Australia, Great Britain, and the United States. There are also specific regional locales for Australian English, British English, U.S. English, and so on.

When data is displayed to a user it should be formatted according to the conventions of the user’s native country, region, or culture. Conversely, when users enter data, they may do so according to their own customs or preferences. Locale objects are used to provide information required to localize the presentation or interpretation of data. This information can include decimal separators, date formats, and units of measurement, as well as language and region information.

Locales are arranged in a hierarchy. At the root is the system locale, which provides default values for all settings. Below the root hierarchy are language locales. These encapsulate settings for language groups, such as English, German and Chinese (using identifiers `en`, `de`, and `zh`). Normal locales specify a language in a particular region (e.g., `en-GB`, `de-AT`, and `zh-SG`).

A locale is expressed by a ISO 639-3 alpha-3 code element, optionally followed by a dash character `-` and an ISO 3166-1 alpha-2 code. 

For example: `eng` (which denotes a standard English), `eng-US` (which denotes an American English).

Write a class `Locale` that represents a tag respecting [RFC 4646](https://tools.ietf.org/html/rfc4646). The constructor of this class takes two arguments:

- `language_code`: An ISO 639-3 alpha-3 code (or alpha-2 code; which will be automatically converted to its equivalent ISO 639-3 alpha-3 code).
- `country_code` (optional): An ISO 3166-1 alpha-2 code.

The string representation of an object `Locale` corresponds to the ISO 639-3 alpha-3 code, optionally followed by a dash character `-` and an ISO 3166-1 alpha-2 code, of this locale.

Add the static method `from_string` that takes an argument `locale`, a string representation of a locale, i.e., an ISO 639-3 alpha-3 code (or alpha-2 code), optionally followed by a dash character `-` and an ISO 3166-1 alpha-2 code. The method `from_string` returns an object `Locale`.

For example:

```python
>>> locale = Locale('vie')
>>> str(locale)
'vie'
>>> locale = Locale.from_string('fr-CA')
>>> str(locale)
'fra-CA'
```

### Label

A label corresponds to a humanly-readable textual content written in a given locale (English by default).

Write a class `Label` that takes two arguments:

- `content`: Humanly-readable textual content of the label.
- `locale` (optional): An object `Locale` identifying the language of the textual content of this label (English by default).

Add two read-only properties `content` and `locale` that respectively returns the humanly-readable textual content of the label and the object `Locale` representing the locale which the content is written in.

For example:

```python
>>> label = Label("Hello, World!")
>>> label.content
'Hello, World!'
>>> type(label.locale)
<class 'Locale'>
>>> str(label.locale)
'eng'
>>> label = Label("Rạch Bến Nghé, Bến Chương Dương", Locale('vie'))
>>> label.content
'Rạch Bến Nghé, Bến Chương Dương'
>>> str(label.locale)
'vie'
```

### Photo Title

Add a read-only property `title` to the class `FlickrPhoto` that returns the label of the photo.

For example:

```python
>>> photo = FlickrPhoto('49510908217', "SAIGON 1974 - Rạch Bến Nghé, Bến Chương Dương")
>>> photo.title
<Label object at 0x107b6a390>
>>> photo.title.content
'SAIGON 1974 - Rạch Bến Nghé, Bến Chương Dương'
>>> photo.title.locale
vie
```

## Waypoint 5: Browse the Photos of a Flickr User

Add an instance method `get_photos` to the class `FlickrApi` that takes the following arguments:

- `user_id`: The identification of a Flickr user.
- `page`: An integer representing the page of the user's photostream to return photos. If this argument is omitted, it defaults to `1`.
- `per_page`: An integer representing the number of photos to return per page. If this argument is omitted, it defaults to `100`. The maximum allowed value is `500`.

The method `get_photos` returns a tuple of values:

- A list of objects `FlickrObjects`.
- An integer representing the number of pages of `per_page` photos in the user's photostream.
- An integer representing the total number of photos in the user's photostream.

For example:

```python
>>> photos, page_count, photo_count = flickr_api.get_photos('13476480@N07', page=10, per_page=5)
>>> page_count
20380
>>> photo_count
101899
>>> print('\n'.join([f'({photo.id}) {photo.title.content}' for photo in photos]))
(49499522706) SAIGON 1938 - Nhà rồng (trụ sở hãng vận tải biển Messageries Maritimes tại Saigon)
(49499024083) HẢI PHÒNG 1938 - Trụ sở hãng vận tải biển Messageries Maritimes tại Hải Phòng
(49496075888) HANOI 1973 - Góc Phố Đinh Tiên Hoàng-Hàng Khay
(49501365086) Phố Đinh Tiên Hoàng & Đồng Khánh HANOI
(49496564661) HANOI 1973 - Cửa hàng Bách hóa Tổng hợp, góc Phố Tràng Tiền & Phố Hàng Bài
```

## Waypoint 6: Find Highest Resolution Photo

A Flickr photo can have several sizes (resolutions). You can get the list of available sizes for a given photo by calling the method [`flickr.photos.getSizes`](https://www.flickr.com/services/api/flickr.photos.getSizes.html).

For example:

```json
{
  "sizes": {
    "canblog": 0,
    "canprint": 0,
    "candownload": 1,
    "size": [
      {
        "label": "Square",
        "width": 75,
        "height": 75,
        "source": "https://live.staticflickr.com/65535/49499525286_e6f0b9d940_s.jpg",
        "url": "https://www.flickr.com/photos/13476480@N07/49499525286/sizes/sq/",
        "media": "photo"
      },
      {
        "label": "Large Square",
        "width": "150",
        "height": "150",
        "source": "https://live.staticflickr.com/65535/49499525286_e6f0b9d940_q.jpg",
        "url": "https://www.flickr.com/photos/13476480@N07/49499525286/sizes/q/",
        "media": "photo"
      },
      {
        "label": "Thumbnail",
        "width": 96,
        "height": 100,
        "source": "https://live.staticflickr.com/65535/49499525286_e6f0b9d940_t.jpg",
        "url": "https://www.flickr.com/photos/13476480@N07/49499525286/sizes/t/",
        "media": "photo"
      },
      {
        "label": "Small",
        "width": "230",
        "height": "240",
        "source": "https://live.staticflickr.com/65535/49499525286_e6f0b9d940_m.jpg",
        "url": "https://www.flickr.com/photos/13476480@N07/49499525286/sizes/s/",
        "media": "photo"
      },
      {
        "label": "Small 320",
        "width": "307",
        "height": "320",
        "source": "https://live.staticflickr.com/65535/49499525286_e6f0b9d940_n.jpg",
        "url": "https://www.flickr.com/photos/13476480@N07/49499525286/sizes/n/",
        "media": "photo"
      },
      {
        "label": "Small 400",
        "width": "383",
        "height": "400",
        "source": "https://live.staticflickr.com/65535/49499525286_e6f0b9d940_w.jpg",
        "url": "https://www.flickr.com/photos/13476480@N07/49499525286/sizes/w/",
        "media": "photo"
      },
      {
        "label": "Medium",
        "width": "479",
        "height": "500",
        "source": "https://live.staticflickr.com/65535/49499525286_e6f0b9d940.jpg",
        "url": "https://www.flickr.com/photos/13476480@N07/49499525286/sizes/m/",
        "media": "photo"
      },
      {
        "label": "Medium 640",
        "width": "613",
        "height": "640",
        "source": "https://live.staticflickr.com/65535/49499525286_e6f0b9d940_z.jpg",
        "url": "https://www.flickr.com/photos/13476480@N07/49499525286/sizes/z/",
        "media": "photo"
      },
      {
        "label": "Medium 800",
        "width": "767",
        "height": "800",
        "source": "https://live.staticflickr.com/65535/49499525286_e6f0b9d940_c.jpg",
        "url": "https://www.flickr.com/photos/13476480@N07/49499525286/sizes/c/",
        "media": "photo"
      },
      {
        "label": "Large",
        "width": "981",
        "height": "1024",
        "source": "https://live.staticflickr.com/65535/49499525286_e6f0b9d940_b.jpg",
        "url": "https://www.flickr.com/photos/13476480@N07/49499525286/sizes/l/",
        "media": "photo"
      },
      {
        "label": "Large 1600",
        "width": "1533",
        "height": "1600",
        "source": "https://live.staticflickr.com/65535/49499525286_aaee644fd2_h.jpg",
        "url": "https://www.flickr.com/photos/13476480@N07/49499525286/sizes/h/",
        "media": "photo"
      },
      {
        "label": "Original",
        "width": "1533",
        "height": "1600",
        "source": "https://live.staticflickr.com/65535/49499525286_7df8ab7063_o.jpg",
        "url": "https://www.flickr.com/photos/13476480@N07/49499525286/sizes/o/",
        "media": "photo"
      }
    ]
  },
  "stat": "ok"
}
```

We will only need to download the highest resolution of a photo.

Write a class `FlickrPhotoSize` that provides the information of a given size of a photo:

- `label`: The label representing the size of a photo.
- `width`: The number of pixel columns of the photo for this size.
- `height`: The number of pixel rows of the photo for this size.
- `url`: The Uniform Resource Locator (URL) that references the image file of the photo for this size.

Add a static method `get_photo_sizes` to the class `FlickrApi` that returns a list of objects `FlickrPhotoSize`. This method **MUST** use the Flickr API [`flickr.photos.getSizes`](https://www.flickr.com/services/api/flickr.photos.getSizes.html):

For example:

```python
>>> sizes = flickr_api.get_photo_sizes('49499522706')
>>> print('\n'.join([f'- {size.label}: {size.width}x{size.height} ({size.url})' for size in sizes]))
- Square: 75x75 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_s.jpg)
- Large Square: 150x150 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_q.jpg)
- Thumbnail: 95x100 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_t.jpg)
- Small: 228x240 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_m.jpg)
- Small 320: 304x320 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_n.jpg)
- Small 400: 381x400 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_w.jpg)
- Medium: 476x500 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca.jpg)
- Medium 640: 609x640 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_z.jpg)
- Medium 800: 761x800 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_c.jpg)
- Large: 974x1024 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_b.jpg)
- Large 1600: 1522x1600 (https://live.staticflickr.com/65535/49499522706_c7e9e70192_h.jpg)
- Original: 1522x1600 (https://live.staticflickr.com/65535/49499522706_edb7355245_o.jpg)
```

Add a read-write property `sizes` to the class `FlickrPhoto` that sets/returns the list of available sizes of the photo. Also add a read-only property `best_size` that returns the size that has the highest resolution.

For example:

```python
>>> photos, page_count, photo_count = flickr_api.get_photos('13476480@N07')
>>> photo = photos[0]
>>> photo.id
'49513950058'
>>> sizes = flickr_api.get_photo_sizes(photo.id)
>>> photo.title.content
'LAI THIEU 1974 - Fabrication de poteries'
>>> print('\n'.join([f'- {size.label}: {size.width}x{size.height} ({size.url})' for size in sizes]))
- Square: 75x75 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_s.jpg)
- Large Square: 150x150 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_q.jpg)
- Thumbnail: 95x100 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_t.jpg)
- Small: 228x240 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_m.jpg)
- Small 320: 304x320 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_n.jpg)
- Small 400: 381x400 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_w.jpg)
- Medium: 476x500 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca.jpg)
- Medium 640: 609x640 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_z.jpg)
- Medium 800: 761x800 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_c.jpg)
- Large: 974x1024 (https://live.staticflickr.com/65535/49499522706_c629a2f8ca_b.jpg)
- Large 1600: 1522x1600 (https://live.staticflickr.com/65535/49499522706_c7e9e70192_h.jpg)
- Original: 1522x1600 (https://live.staticflickr.com/65535/49499522706_edb7355245_o.jpg)
>>> photo.sizes = size
>>> photo.best_size.width
1522
>>> photo.best_size.height
1600
>>> photo.best_size.url
'https://live.staticflickr.com/65535/49499522706_c7e9e70192_h.jpg'
```

## Waypoint 7: Fetch Photo Description and Comments

Add the instance method `get_photo_description` to the class `FlickrApi` that takes an argument `photo_id` and returns a string representing the description of the photo.

For example:

```python
>>> description, comments = flickr_api.get_photo_info('8967911298')
>>> description
''
>>> len(comments)
5
>>> comments[0]
'.\nnơi này thời Pháp thuộc:\n[http://www.flickr.com/photos/13476480@N07/4722795861/]'
```

![](flickr_photo_49515206006_description.png)

Add the read-write property `description` to the class `FlickrPhoto` that sets/returns the description of the photo. The write property `description` transforms the string argument to an object `Label` that the read property `description` returns.

For example:

```python
>>> photo_id = '49515206006'
>>> photo = FlickrPhoto(photo_id, 'THU DAU MOT - Ecole des enfants de troupe - La gymnastique -')
>>> description = flickr_api.get_photo_description(photo_id)
>>> description
'Giờ thể dục của học sinh trường Thiếu sinh quân\nBinh Duong – Thu Dau Mot\n    Date : 1920-1929'
>>> photo.description = description
>>> photo.description
<Label object at 0x10b69ee80>
>>> photo.description.content
'Giờ thể dục của học sinh trường Thiếu sinh quân\nBinh Duong – Thu Dau Mot\n Date : 1920-1929'
>>> photo.description.locale
'vie'
```

Add the instance method `get_photo_comments` to the class `FlickrApi` that takes an argument `photo_id` and returns a list of strings corresponding to the comments posted to the photo. Add the read-write property `comments` to the class `FlickrPhoto` that sets/returns the comments of the photo. The write property `comments` transforms the list of strings argument to a list of objects `Label` that the read property `comments` returns.

_Note: We only need to store the textual content of the comments posted to the photo; we don't need the name of the user who posted the comment, nor do we need to store the date when the comment was posted._

For example:

```python
>>> photo_id = '8967911298'
>>> photo = FlickrPhoto(photo_id, 'CHOLON 1950 - Vòng xoay giao lộ Khổng Tử - Tổng Đốc Phương (ngã 5 Cholon)')
>>> comments = flickr_api.get_photo_comments(photo_id)
>>> photo.comments = comments
>>> photo.comments
[<Label object at 0x106880860>, <Label object at 0x1068a1198>, <Label object at 0x10b69c908>, <Label object at 0x10b4872e8>, <Label object at 0x10b4879e8>]
>>> photo.comments[0].content
'.\nnơi này thời Pháp thuộc:\n[http://www.flickr.com/photos/13476480@N07/4722795861/]'
>>> photo.comments[0].locale
vie
```

![](flickr_photo_8967911298_comments.png)

## Waypoint 8: Command-line Interface Arguments

We would like our script to support several features such as, to allow our users to mirror images only, information (i.e.,title, description, comments) only, or both.

The user needs be able to specify these options (**parameters**) in our script. Our script needs to parse these options from the command-line. This is what the Python library [argparse](https://docs.python.org/3/library/argparse.html) is used for.

Update your script to support the [command-line parameters](https://docs.python.org/3.8/howto/argparse.html) defined below. Some parameters are required, others are optional with default values.

- `--username` (required): Username of the account of a user on Flickr
- `--cache_path` (optional): Specify the absolute path where the script saves photos downloaded from Flickr. It defaults to `~/.flickr/`.
- `--consumer-key` (optional): Flickr API key that our script will use to connect to the Flickr server;
- `--consumer-secret` (optional): Flickr API secret that our script will use to encode a request to be sent to the Flickr server;
- `--save-api-keys` (optional): Specify whether to save the Flickr API keys for further usage. It defaults to `False`.
- `--image-only` (optional): Specify whether the script must only download photos' images. It defaults to `False`.
- `--info-only` (optional): Specify whether the script must only download photos' information. It defaults to `False`.
- `--info-level` (optional): Specify the level of information of a photo to fetch:
  - `0` (default): Title only;
  - `1`: Title and description;
  - `2`: Title, description, and comments.

```bash
$ ./flickr.py --help
usage: flickr.py [-h] [--consumer-key CONSUMER KEY]
                 [--consumer-secret CONSUMER SECRET] [--cache-path CACHE PATH]
                 [--image-only] [--info-level LEVEL] [--info-only]
                 [--save-api-keys] --username USERNAME

Flickr Mirroring

optional arguments:
  -h, --help            show this help message and exit
  --cache-path CACHE PATH
                        specify the absolute path where the photos downloaded
                        from Flickr need to be cached
  --consumer-key CONSUMER KEY
                        a unique string used by the Consumer to identify
                        themselves to the Flickr API
  --consumer-secret CONSUMER SECRET
                        a secret used by the Consumer to establish ownership
                        of the Consumer Key
  --image-only          specify whether the script must only download photos'
                        images
  --info-level LEVEL    specify the level of information of a photo to fetch
                        (value between 0 and 2)
  --info-only           specify whether the script must only download photos'
                        information
  --save-api-keys       specify whether to save the Flickr API keys for
                        further usage
  --username USERNAME   username of the account of a user on Flickr to mirror
                        their photostream
```

For example:

 The command-line executes our script, specifying to mirror photos from username `manhhai`, providing fake Flickr API keys, and specifying to fetch both images and information of photos (default), but to limit the information of the photos to title and description only (no comments):

```bash
$ ./flickr.py  --username manhhai --consumer-key foo --consumer-secret bar --info-level 2
```

Add a function `get_arguments()` in your script `flickr.py` that [reads the parameters](https://realpython.com/command-line-interfaces-python-argparse/) passed onto the command-line and returns an object [`Namespace`](https://docs.python.org/3/library/argparse.html#argparse.Namespace) that holds these attributes.

We will see later in this mission how to process these parameters.

## Waypoint 9: Flickr API Keys

Our script needs Flickr keys to send requests to Flickr API servers.

### Security Issue with Command-Line Parameters

We can pass these keys on the command-line, which is okay if you are executing the script on your personal computer, but which is [not secured](https://www.netmeister.org/blog/passing-passwords.html) if you are executing the script on a server. These keys must **NOT** be revealed to anyone who would be able to connect to this server.

The Unix command `sh`, short for Process Status, displays information related to the processes running on the system.
Running this command with the argument `-eax` will display information about other users' processes, providing the command has been executed for each of them, and so revealing all the arguments that have been passed along each command.

For example:
 If you were running your script with the following command on a Linux server:

```bash
$ ./flickr.py --username manhhai --consumer-key fc8f309af6bf69bfea94628bce11eadb --consumer-secret 866597e43a98c8c5
```

Anyone who would have access to this server, would be able to view the Flickr API keys you have passed to your running script:

```bash
$ ps -eax | grep flickr
14672 ttys009    0:16.89 python ./flickr.py --username manhhai --consumer-key fc8f309af6bf69bfea94628bce11eadb --consumer-secret 866597e43a98c8c5
```

### Prompting for API Keys

The parameters `--consumer-key` and `--consumer-secret` are a facility to pass your Flickr API key to your script that runs on your personnal computer, but another method should be used to provide these keys if you are running your script on a server. A more secure way is that your script [prompts the user to manually enter](https://docs.python.org/3/library/functions.html#input) the keys:

```bash
$ ./flickr.py --username manhhai
Enter your Flickr API key: fc8f309af6bf69bfea94628bce11eadb
Enter your Flickr API secret: 866597e43a98c8c5
```

_Note: An even more secure method is to use the Python Standard Library module [`getpass`](https://docs.python.org/3.8/library/getpass.html) to prompt the user for a sensitive date **without echoing**._

### Saving API Keys to a Secured File

However, prompting the user each time they execute your script is annoying. The script should save these keys in a file whose permission access is restricted to the current Unix user, and reads these keys from this file when it exists.

```bash
$ ./flickr.py --username manhhai --save-api-keys
Enter your Flickr API key:
Enter your Flickr API secret:
```

Our script creates a file `flickr_keys`, in the folder specified by the parameter `--cache-path` (default ``~/.flickr`). The permissions of this file is set so that the file is [only accessible by our Unix user (**owner**)](https://chmod-calculator.com/).

```bash
$ ls -la ~/.flickr/flickr_keys
-rw-------  1 intek  staff  91 Mar 19 11:20 /home/intek/.flickr/flickr_keys
```

Our script writes a JSON expression containing the attributes `consumer_key` and `consumer_secret` with the values we have entered when the script prompted us for our Flickr keys:

```bash
$ cat ~/.flickr/flickr_keys | json_pp
{
   "consumer_secret" : "866597e43a98c8c5",
   "consumer_key" : "fc8f309af6bf69bfea94628bce11eadb"
}
```

When we execute our script one more time, without passing the parameters `--consumer-key` and `--consumer-secret`, our script tries to read these keys from the file `flickr_keys`, if it exists. If no keys are found, our script prompts us to enter the keys.

Update the script `flickr.py` so that it gets the Flickr API keys using the following methods in the following order:

1. Read the arguments passed to the script from the command line;
1. Use the keys previously specified and stored in the file `flickr_key`, located by default in the cache folder specified by the comand-line argument `--cache-path`;
1. Request the user to input the keys.

The script `flickr.py` stores the keys in the file `flickr_key` if the command-line parameter `--save-api-keys` is specified.

# Mirroring User Photostream

## Waypoint 10: User Photostream Mirroring Agent

Write a class `FlickrUserPhotostreamMirroringAgent` in the script `flickr.py` whose constructor takes the following arguments:

- `username` (required): Username of the account of a user on Flickr to mirror their photostream.
- `flickr_consumer_key` (required): A unique string used by the Consumer to identify themselves to the Flickr API.
- `flickr_consumer_secret` (required): A secret used by the Consumer to establish ownership of the Consumer Key.
- `cache_root_path_name` (optional): Specify the absolute path where the images and/or information of the photos downloaded from Flickr need to be stored.
- `cache_directory_depth` (optional): Number of sub-directories the cache file system is composed of (i.e., its depth, to store photo files into the child directories, the leaves, of this cache). We will see this parameter later in this mission.
- `image_only` (optional): Specify whether the script must only download photos' images.
- `info_level` (optional): Specify the level of information of a photo to fetch (value between `0` and `2`)
- `info_only` (optional): Specify whether the agent must only download photos' information.

Add a read-only property `user` to the class `FlickrUserPhotostreamMirroringAgent` that returns an object `FlickrUser` representing the user whose photostream is going to be mirrored by the instance of the class `FlickrUserPhotostreamMirroringAgent`.

For example:

```python
>>> mirroring_agent = FlickrUserPhotostreamMirroringAgent(
...     'manhhai',
...     'fc8f309af6bf69bfea94628bce11eadb',
...     '866597e43a98c8c5')
>>> mirroring_agent.user
<FlickrUser object at 0x11011ae10>
>>> mirroring_agent.user.id
'13476480@N07'
>>> mirroring_agent.user.username
'manhhai'
```

Add an instance method `run` to the class `FlickrUserPhotostreamMirroringAgent`. This method will be invoked by your script to start mirroring the user's photostream.

## Waypoint 11: Cache Filesystem Structure

The Flickr photostream of a user can contain hundreds of thousands of photos. Flickr pro accounts get unlimited storage.

Storing many files in one folder (**flat directory structure**) is **not a good idea at all**. You would see a [serious performance hit](https://medium.com/@hartator/benchmark-deep-directory-structure-vs-flat-directory-structure-to-store-millions-of-files-on-ext4-cac1000ca28) of your machine's file system. It's advisable to split them down into folders (**deep directory structure**).

Instead of storing all the files (images and information) of the photo, fetched from the user's photostream, into a flat directory like this one:

```text
0219d7ae66b30abddafcf951d3425a9a.jpg
0219d7ae66b30abddafcf951d3425a9a.json
02b327dcb38a3f56a2fd307942b0c8ec.jpg
02b327dcb38a3f56a2fd307942b0c8ec.json
02cf1dad45db0addc14e5b069df09494.jpg
02cf1dad45db0addc14e5b069df09494.json
03383a02e239d5cca8f3d68242a6ba12.jpg
03383a02e239d5cca8f3d68242a6ba12.json
04123540e53b7cbcd40e1189e1de5ec2.jpg
04123540e53b7cbcd40e1189e1de5ec2.json
05b3d86c470f9af75bf9ebfaeb0acd61.jpg
05b3d86c470f9af75bf9ebfaeb0acd61.json
076f83d3c0df693aa2d43f2853bb11f3.jpg
076f83d3c0df693aa2d43f2853bb11f3.json
07d955375e1ee02255e41557a3e32299.jpg
07d955375e1ee02255e41557a3e32299.json
0906403323ab410f1effc697cd180d0b.jpg
0906403323ab410f1effc697cd180d0b.json
09e973bbcdee19c4f60e60d79b64a080.jpg
09e973bbcdee19c4f60e60d79b64a080.json
(...)
```

(...) a better option is to split these files into a deep directory structure like this one:

```text
.
├── 0
│   ├── 2
│   │   ├── 1
│   │   │   └── 9
│   │   │       ├── 0219d7ae66b30abddafcf951d3425a9a.jpg
│   │   │       └── 0219d7ae66b30abddafcf951d3425a9a.json
│   │   ├── b
│   │   │   └── 3
│   │   │       ├── 02b327dcb38a3f56a2fd307942b0c8ec.jpg
│   │   │       └── 02b327dcb38a3f56a2fd307942b0c8ec.json
│   │   └── c
│   │       └── f
│   │           ├── 02cf1dad45db0addc14e5b069df09494.jpg
│   │           └── 02cf1dad45db0addc14e5b069df09494.json
│   ├── 3
│   │   └── 3
│   │       └── 8
│   │           ├── 03383a02e239d5cca8f3d68242a6ba12.jpg
│   │           └── 03383a02e239d5cca8f3d68242a6ba12.json
│   ├── 4
│   │   └── 1
│   │       └── 2
│   │           ├── 04123540e53b7cbcd40e1189e1de5ec2.jpg
│   │           └── 04123540e53b7cbcd40e1189e1de5ec2.json
│   ├── 5
│   │   └── b
│   │       └── 3
│   │           ├── 05b3d86c470f9af75bf9ebfaeb0acd61.jpg
│   │           └── 05b3d86c470f9af75bf9ebfaeb0acd61.json
│   ├── 7
│   │   ├── 6
│   │   │   └── f
│   │   │       ├── 076f83d3c0df693aa2d43f2853bb11f3.jpg
│   │   │       └── 076f83d3c0df693aa2d43f2853bb11f3.json
│   │   └── d
│   │       └── 9
│   │           ├── 07d955375e1ee02255e41557a3e32299.jpg
│   │           └── 07d955375e1ee02255e41557a3e32299.json
│   ├── 9
│   │   ├── 0
│   │   │   └── 6
│   │   │       ├── 0906403323ab410f1effc697cd180d0b.jpg
│   │   │       └── 0906403323ab410f1effc697cd180d0b.json
│   │   └── e
│   │       └── 9
│   │           ├── 09e973bbcdee19c4f60e60d79b64a080.jpg
│   │           └── 09e973bbcdee19c4f60e60d79b64a080.json
(...)
```

Add a private instance method `__download_photo_image` to the class `FlickrUserPhotostreamMirroringAgent` that takes a required argument `photo` (an object `Photo`). This function downloads the **best resolution image** of the photo into the local cache using a **deep directory structure**, under a sub-folder named after the username of the Flickr user.

For example:

```python
>>> mirroring_agent = FlickrUserPhotostreamMirroringAgent(
...     'manhhai',
...     'fc8f309af6bf69bfea94628bce11eadb',
...     '866597e43a98c8c5')
>>> photo = FlickrPhoto('49674775373', Label('Huế 1920-1929 - Chez un grand mandarin : avant le repas', Locale('fra')))

# Fake method call (this is a private method!) just for the example
>>> mirroring_agent.__download_photo_image(photo)
>>> photo.best_size.url
'https://live.staticflickr.com/65535/49674775373_689e7ad3a2_3k.jpg'
>>> photo.image_filename
'fb2e16023f14649810da65b5fcbea02e.jpg'
```

The function has downloaded the image file of this photo and stored this file under the following path with a depth of `4`:

```bash
$ find . -name fb2e16023f14649810da65b5fcbea02e.jpg
./.flickr/manhai/f/b/2/e/fb2e16023f14649810da65b5fcbea02e.jpg
```

The depth of the directory structure is specified by the user by passing the parameter `cache_directory_depth` when executing the script from the command-line. It defaults to `4`.

## Waypoint 12: Mirroring Loop & Cache Strategies

### Flickr Page Numbering

The photostream of a Flickr user is a collection of photos. A Flickr user adds more and more photos to their collection.

Flickr sorts the photos of a user's photostream by their chronological order (e.g., the time when the user has uploaded these photos to Flickr).

The Flickr API splits these photos down into [logical (virtual)](https://www.pcmag.com/encyclopedia/term/logical-vs-physical) pages of `100` photos (by default). A page is just a view of a group of photos. These pages are numbered from `1` to `n`.

You might think that the first page corresponds to the first photos that were uploaded to Flickr. However, Flickr actually uses an inverse chronological order (inverse timeline): Flickr arranges pages from the earliest to the oldest uploaded photos. The first page always contains the most recent photos published by the user, while the last page contains the first photos that were uploaded by the user.

This means that the content of each page (the list of photos that a page references) changes whenever the user uploads more photos.

![Flickr Page Numbering](flickr_page_numbering.jpg)

### Photostream Reading Methods

We can adopt two methods to read and cache the photostream of a user: [FIFO and LIFO](https://www.youtube.com/watch?v=D_kGsCa2T1k).

#### First-In First-Out

The first method consists of reading a user's photostream from their first published photos to the most recent (e.g., reading from the current last page of the user's photostream to the current first page). This method is similar to the [First-In First-Out (FIFO)](<https://en.wikipedia.org/wiki/FIFO_(computing_and_electronics)>) principle.

![FIFO Strategy](fifo_strategy.jpg)

Let's suppose that our script downloads the first 4 photos `A`, `B`, `C`, and `D` published by a user to their photostream and stops for whatever reason (network outage, crash, user interruption, etc.). When our script is executed again, it automatically continues downloading photos from the 5th photo `E` of the user's photostream.

In the meantime, if the user adds more photos to their photostream, this has no impact to the FIFO strategy except that the page numbering will change, and our script needs to handle this new numbering.

#### Last-In First-Out

The second method consists of reading a user's photostream from their most recent published photo to their first published photos (e.g., reading from the first page of the user's photostream to the last page). This method is similar to the [Last-In First-Out (LIFO)](<https://en.wikipedia.org/wiki/Stack_(abstract_data_type)>) principle.

![LIFO Strategy](lifo_strategy.jpg)

Let's suppose that our script downloads the 4 most recent photos `R`, `Q`, `P`, and `O` and stops. When our script is executed again, it automatically continues downloading photos from the earliest not already downloaded, such has `N`, etc.

However, if the user has added new photos `S` and `T` to their photostream in the meantime, our script starts downloading these most recent photos (`S` and `T`), before continuing with the earliest not already downloaded, such as `N`.

### Caching Strategy Implementation

#### Caching Strategy Selection

Add support for the command-line parameters `--fifo` and `--lifo` to your script:

```bash
usage: flickr.py [-h] [--cache-path CACHE PATH] [--consumer-key CONSUMER KEY]
                 [--consumer-secret CONSUMER SECRET] [--fifo] [--image-only]
                 [--info-level LEVEL] [--info-only] [--lifo] [--save-api-keys]
                 --username USERNAME

Flickr Mirroring

optional arguments:
  -h, --help            show this help message and exit
  --cache-path CACHE PATH
                        specify the absolute path where the images and/or
                        information of the photos downloaded from Flickr need
                        to be cached
  --consumer-key CONSUMER KEY
                        a unique string used by the Consumer to identify
                        themselves to the Flickr API
  --consumer-secret CONSUMER SECRET
                        a secret used by the Consumer to establish ownership
                        of the Consumer Key
  --fifo                specify the First-In First-Out method to mirror the
                        user's photostream, from the oldest uploaded photo to
                        the earliest
  --image-only          specify whether the script must only download photos'
                        images
  --info-level LEVEL    specify the level of information of a photo to fetch
                        (value between 0 and 2)
  --info-only           specify whether the script must only download photos'
                        information
  --lifo                specify the Last-In First-Out method to mirror the
                        user's photostream, from the earliest uploaded photo
                        to the oldest (default option)
  --save-api-keys       specify whether to save the Flickr API keys for
                        further usage
  --username USERNAME   username of the account of a user on Flickr to mirror
                        their photostream
```

Add an [enumeration](https://docs.python.org/3/library/enum.html) `CachingStrategy` to your script. This enumeration declares the following items:

- `FIFO`: First-In First-Out method consists of downloading photos from the oldest published by the user to the most recent.
- `LIFO`: Last-In First-Out method consists in downloading photos from the most recent photo published by the user to the oldest.

For example:

```python
>>> CachingStrategy
<enum 'CachingStrategy'>
>>> CachingStrategy.FIFO
<CachingStrategy.FIFO: 1>
>>> CachingStrategy.LIFO
<CachingStrategy.LIFO: 2>
```

Update the constructor of the class `FlickrUserPhotostreamMirroringAgent` to accept another optional argument `caching_strategy` (an item of the enumeration `CachingStrategy`). This argument defaults to `CachingStrategy.LIFO`.

_Note: Some users will prefer the LIFO caching strategy as this method fetches the most recent published photos first. These users get fresher photos right away instead of waiting for the photostream to be fully mirrored._

#### Mirroring Loop with Selected Cache Strategy

Update the instance method `run` of the class `FlickrUserPhotostreamMirroringAgent` to download photos according to the specified caching strategy.

**IMPLEMENT A SIMPLISTIC FIRST VERSION THAT ONLY DOWNLOADS PHOTO IMAGES. WE CONSIDER THAT THE USER'S PHOTOSTREAM DOESN'T CHANGE WHILE YOUR SCRIPT IS RUNNING: THE USER DOESN'T ADD OR REMOVE ANY PHOTOS TO/FROM THEIR PHOTOSTREAM.**

For example, using the default LIFO caching strategy:

```python
>>> mirroring_agent = FlickrUserPhotostreamMirroringAgent(
...     'manhhai',
...     'fc8f309af6bf69bfea94628bce11eadb',
...     '866597e43a98c8c5')
>>> mirroring_agent.run()
2020-03-23 08:43:28,596 [INFO] Scanning page 1/1026...
2020-03-23 08:43:28,599 [INFO] Caching image of photo 9b6f41df42e96cbb26e2c3d83c85a8b5...
2020-03-23 08:43:31,486 [INFO] Caching image of photo b882e2689990974d7b2690730c26235a...
2020-03-23 08:43:33,391 [INFO] Caching image of photo f577355eeeeb6abb4fd138efdc9dd6f5...
2020-03-23 08:43:35,419 [INFO] Caching image of photo 0fd39acd5d5db776ea4a9cde2a266671...
2020-03-23 08:43:37,484 [INFO] Caching image of photo 28f3f44801b622ee8d4117e9a2d5bf21...
2020-03-23 08:43:39,771 [INFO] Caching image of photo 67d8f7981fa5f63e7cb1437217e98785...
```

```bash
$ tree ~/.flickr/manhhai
/home/intek/.flickr/manhhai
├── 0
│   └── f
│       └── d
│           └── 3
│               └── 0fd39acd5d5db776ea4a9cde2a266671.jpg
├── 2
│   └── 8
│       └── f
│           └── 3
│               └── 28f3f44801b622ee8d4117e9a2d5bf21.jpg
├── 6
│   └── 7
│       └── d
│           └── 8
│               └── 67d8f7981fa5f63e7cb1437217e98785.jpg
├── 9
│   └── b
│       └── 6
│           └── f
│               └── 9b6f41df42e96cbb26e2c3d83c85a8b5.jpg
├── b
│   └── 8
│       └── 8
│           └── 2
│               └── b882e2689990974d7b2690730c26235a.jpg
└── f
    └── 5
        └── 2
            └── 7
                └── f5275b3940b714fdb083995086ca2b83.jpg

29 directories, 16 files
```

Similarily, using the FIFO caching strategy:

```python
>>> mirroring_agent = FlickrUserPhotostreamMirroringAgent(
...     'manhhai',
...     'fc8f309af6bf69bfea94628bce11eadb',
...     '866597e43a98c8c5',
...     caching_strategy=CachingStrategy.FIFO)
>>> mirroring_agent.run()
2020-03-23 10:34:45,467 [INFO] Scanning page 1026/1026...
2020-03-23 10:34:45,467 [INFO] Caching image of photo ba892a4943e1c1dd07379f92068eac7e...
2020-03-23 10:34:46,821 [INFO] Caching image of photo efd816c67a2bbd8eb47559c2a98b0320...
2020-03-23 10:34:47,680 [INFO] Caching image of photo 134d76e411acef10089b17e532b7245f...
2020-03-23 10:34:48,907 [INFO] Caching image of photo a38c7c8156c8fbe309d354f750c4880d...
2020-03-23 10:34:50,100 [INFO] Caching image of photo e8ad574c0f4733fc116c6f1c9cb92035...
2020-03-23 10:34:50,950 [INFO] Caching image of photo ff61ebe4fac3f22f07da55f9810d65c6...
```

If you stop and rerun your script, it will start downloading the most recent photo not already cached:

```bash
$ ./flickr.py --username manhhai --lifo
2020-03-23 08:49:27,630 [INFO] Scanning page 1/1026...
2020-03-23 08:43:40,648 [INFO] Caching image of photo 6dbf9c52ccec1722e32161cd41d6a290...
2020-03-23 08:43:41,546 [INFO] Caching image of photo f5275b3940b714fdb083995086ca2b83...
2020-03-23 08:49:27,660 [INFO] Caching image of photo ee6557cf53ebcfdbd66c617ca9e6c75f...
2020-03-23 08:49:32,540 [INFO] Caching image of photo 0e35aa2fab6527ebc98cc7a285d2cc12...
2020-03-23 08:49:33,637 [INFO] Caching image of photo 397d6bc91f7f6642373a5323dea291fb...
```

## Waypoint 13: Fine-Grain Mirroring

We haven't yet integrated the real usage of the command-line arguments `--image-only`, `--info-only`, and `--info-level`. We have only focused so far on downloading photo images.

Update your script to fetch photos' image and/or info according to the arguments passed on the command-line.

- `--image-only`: Download images only.
- `--info-only`: Fetch info only.

If the argument `--image-only` is not specified, the argument `--info-level` indicates the level of information to fetch from a photo:

- `0` (default): The title of the photo only.
- `1`: The title and the description of the photo.
- `2`: The title, the description, and the textual content of the comments of the photo.

For example:

```bash
$ ./flickr.py --username manhhai --save-api-keys --fifo --info-only --info-level 2
2020-03-23 12:16:30,560 [INFO] Scanning page 1026/1026...
2020-03-23 12:16:32,919 [INFO] Caching information of photo 576b89d947576c3cb6c72cbbf7e3107a...

$ cat ~/.flickr/manhhai/5/7/6/b/576b89d947576c3cb6c72cbbf7e3107a.json | json_pp
{
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

Flickr supports different endpoints (API methods) to fetch the description of a photo and the comments posted to this photo. It is indeed very important that your script optimizes the number of requests to the Flickr API. Your script **MUST NOT** uselessly fetch data that it won't use. This would be a waste of time and resources (CPU, network bandwidth, and memory).

## Waypoint 14: Mirroring Optimization Strategy with Volatile Photostream

We have implemented a caching strategy (using either FIFO or LIFO method) to avoid repeatedly downloading photos' image and information each time we execute our script:

```bash
$ ./flickr.py --username manhhai
2020-03-23 18:25:41,743 [INFO] Scanning page 1/1026...
2020-03-23 18:25:42,519 [INFO] Scanning page 2/1026...
2020-03-23 18:25:43,331 [INFO] Scanning page 3/1026...
2020-03-23 18:25:43,894 [INFO] Scanning page 4/1026...
2020-03-23 18:25:45,051 [INFO] Scanning page 5/1026...
2020-03-23 18:25:45,591 [INFO] Scanning page 6/1026...
2020-03-23 18:25:46,152 [INFO] Scanning page 7/1026...
2020-03-23 18:25:46,703 [INFO] Scanning page 8/1026...
2020-03-23 18:25:47,965 [INFO] Scanning page 9/1026...
2020-03-23 18:25:49,116 [INFO] Scanning page 10/1026...
2020-03-23 18:25:49,118 [INFO] Caching image of photo 005783b28d7048a16ec730bf38f9ab8e...
2020-03-23 18:25:49,830 [INFO] Caching information of photo 005783b28d7048a16ec730bf38f9ab8e...
2020-03-23 18:25:51,644 [INFO] Caching image of photo 99e41f2d8a84aa3793eaf8738ae8143b...
2020-03-23 18:25:53,663 [INFO] Caching information of photo 99e41f2d8a84aa3793eaf8738ae8143b...
2020-03-23 18:25:53,671 [INFO] Caching image of photo d467d176c2211894eda43c6f3f1639ec...
2020-03-23 18:25:54,477 [INFO] Caching information of photo d467d176c2211894eda43c6f3f1639ec...
2020-03-23 18:25:54,483 [INFO] Caching image of photo 4a1bd124698b8df8453ad723d273191a...
```

It works well, but this is not optimal: our script fetches every page from the beginning (or the end) of the user's photosteam to find which photos have not been cached. This is a huge waste of time! When our script is executed, our script should jump directly to the last page visited where there are photos that it has not processed yet.

However, the photostream of a user is not **immutable**, but **volatile**: the user may add photos between two consecutive executions of our script, and even while our script is running. The number of photos may increase. Photos may slide from one page to another. The number of pages may increase.

**NOTE: WE CONSIDER THAT A FLICKR USER NEVER DELETES PHOTOS FROM THEIR PHOTOSTREAM.**

Update your script so that it only fetches the pages of a user's photostream that it has not completely processed yet.

## Waypoint 15: Package Flickr Mirroring Utility

Package your Flickr mirroring command-line utility and deploy it to the [Python Package Index (PyPI)](https://pypi.org/).

End-users should be able to install it using `pipenv` and run your tool with the Bash command `mirror_flickr`.

For example:

```bash
# Setup a binary directory to install our Flickr mirroring utility
$ mkdir -p ~/.local/bin/intek_flickr_mirroring
$ cd ~/.local/bin/intek_flickr_mirroring

# Setup a Python virtual environment
$ pipenv shell --three
Creating a virtualenv for this project...
Pipfile: /home/intek/.local/bin/intek_flickr_mirroring/Pipfile
Using /usr/local/bin/python3.7 (3.7.4) to create virtualenv...
⠦ Creating virtual environment...Using base prefix '/usr/local'
New python executable in /home/intek/.virtualenvs/intek_flickr_mirroring-wqvphFZ0/bin/python3.7
Also creating executable in /home/intek/.virtualenvs/intek_flickr_mirroring-wqvphFZ0/bin/python
Installing setuptools, pip, wheel...done.
Running virtualenv with interpreter /usr/local/bin/python3.7

✔ Successfully created virtual environment!
Virtualenv location: /home/intek/.virtualenvs/intek_flickr_mirroring-wqvphFZ0
Creating a Pipfile for this project...
Launching subshell in virtual environment...
 . /home/intek/.virtualenvs/intek_flickr_mirroring-wqvphFZ0/bin/activate

# Install our Flickr mirroring utility
(intek_flickr_mirroring) $ pipenv install intek-flickr-mirroring
Installing intek-flickr-mirroring...
Adding intek-flickr-mirroring to Pipfile's [packages]...
✔ Installation Succeeded
Pipfile.lock not found, creating...
Locking [dev-packages] dependencies...
Locking [packages] dependencies...
✔ Success!
Updated Pipfile.lock (96799b)!
Installing dependencies from Pipfile.lock (96799b)...
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 38/38 — 00:00:56

# Execute our Bash script
(intek_flickr_mirroring) $ mirror_flickr --help
usage: mirror_flickr [-h] [--cache-path CACHE PATH]
                     [--consumer-key CONSUMER KEY]
                     [--consumer-secret CONSUMER SECRET] [--debug LEVEL]
                     [--fifo] [--image-only] [--info-level LEVEL]
                     [--info-only] [--lifo] [--save-api-keys] [--verify-image]
                     --username USERNAME

Flickr Mirroring

optional arguments:
  -h, --help            show this help message and exit
  --cache-path CACHE PATH
                        specify the absolute path where the images and/or
                        information of the photos downloaded from Flickr need
                        to be cached
  --consumer-key CONSUMER KEY
                        a unique string used by the Consumer to identify
                        themselves to the Flickr API
  --consumer-secret CONSUMER SECRET
                        a secret used by the Consumer to establish ownership
                        of the Consumer Key
  --debug LEVEL         specify the logging level (value between 0 and 4, from
                        critical to debug)
  --fifo                specify the First-In First-Out method to mirror the
                        user's photostream, from the oldest uploaded photo to
                        the earliest
  --image-only          specify whether the script must only download photos'
                        images
  --info-level LEVEL    specify the level of information of a photo to fetch
                        (value between 0 and 2)
  --info-only           specify whether the script must only download photos'
                        information
  --lifo                specify the Last-In First-Out method to mirror the
                        user's photostream, from the earliest uploaded photo
                        to the lastest (default option)
  --save-api-keys       specify whether to save the Flickr API keys for
                        further usage
  --verify-image        specify whether the script must verify images that
                        have been download
  --username USERNAME   username of the account of a user on Flickr to mirror
                        their photostream
```

Et voilà!
