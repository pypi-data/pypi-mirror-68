# Core Server


## API

### `POST` /upload

Upload an image.

#### parameters

| name        | type | value                                | required |
|:------------|:----:|:------------------------------------:|:--------:|
|description  |string| Image description                    | yes      |
|categorie    |string| Image category                       | yes      |
|operations   |string| List of operations, comma-separated  | no       |
|image        |file  | Image to upload                      | yes      |

