# どうがをぶんかつするやつ

* [Movie extract tool](#movie-extract-tool)
  * [これはなに](#%E3%81%93%E3%82%8C%E3%81%AF%E3%81%AA%E3%81%AB)
  * [なにができるの](#%E3%81%AA%E3%81%AB%E3%81%8C%E3%81%A7%E3%81%8D%E3%82%8B%E3%81%AE)
  * [どうつかうの](#%E3%81%A9%E3%81%86%E3%81%A4%E3%81%8B%E3%81%86%E3%81%AE)
    * [かんきょう](#%E3%81%8B%E3%82%93%E3%81%8D%E3%82%87%E3%81%86)
    * [つかいかた](#%E3%81%A4%E3%81%8B%E3%81%84%E3%81%8B%E3%81%9F)
  * [せいげん](#%E3%81%9B%E3%81%84%E3%81%92%E3%82%93)

## これはなに

OpenCV を利用して動画をフレーム単位の画像に分割するツールです

## なにができるの

以下のことができます

* 動画をPNG画像へ展開する
* 動画の指定範囲だけPNG画像へ展開する
  * フレーム単位で指定
  * 秒単位で指定
* 出力ファイル名の指定
  * フォーマットは `{自由記述}_{index:0>6}.png`
  * 無指定の場合は `{元動画名}_{index:0>6}.png`
* アノテーションファイルを元に動画を分割する

## どうつかうの

### かんきょう

* Python3.6
* OpenCV3
* numpy
* pyyaml
* better_exceptions
* tqdm

Pipenv環境では、 `pipenv install` すればおk

### つかいかた

#### extract_videos_by_anno

アノテーションファイルを元に複数動画を一括処理するやつ (基本こっちを推奨)

```text
python .\extract_videos_by_anno.py -h
usage: extract_videos_by_anno.py [-h] -a ANNOTATION -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -a ANNOTATION, --annotation ANNOTATION
                        annotatiton yaml file
  -o OUTPUT, --output OUTPUT
                        output root dir
```

##### アノテーションファイルの書式

```yaml
- filepath: /path/to/video/file
  sequence:
    - begin: 00:00:00
      end: 00:01:00
      category: normal
    - begin: 00:01:01
      end: 00:02:00
      category: warning
    - begin: 00:02:00
      end: 00:10:00
      category: anomaly
- filepath: /path/to/video/file
  sequence:
    - begin: 00:00:00
      end: 01:00:00
      category: normal
    - begin: 01:01:00
      end: 02:00:00
      category: warning
    - begin: 02:00:00
      end: 10:00:00
      category: anomaly
```

#### extract_video

動画1個を範囲指定して切り出すやつ

```text
python extract_video.py -h
usage: extract_video.py [-h] -i INPUT -o OUTPUT [-b BEGIN] [-e END] [-t]
                        [--base_name BASE_NAME]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input video file
  -o OUTPUT, --output OUTPUT
                        output dir for extracted images
  -b BEGIN, --begin BEGIN
                        extract begin frame or seconds
  -e END, --end END     extract end frame or seconds
  -t, --defined_by_time
                        define begin / end points by time[sec]
  --base_name BASE_NAME
                        base name for saving image, default: input movie name
```

|arguments                |description                                                  |
|-------------------------|-------------------------------------------------------------|
|`-i`, `--input`          |入力元動画ファイル                                           |
|`-o`, `--output`         |画像出力先ディレクトリ                                       |
|`-b`, `--begin`          |分割開始フレーム / 秒 (無指定の場合は最初から)               |
|`-e`, `--end`            |分割終了フレーム / 秒 (無指定の場合は最後まで)               |
|`-t`, `--defined_by_time`|指定した場合は `-b` / `-e` を秒数として解釈                  |
|`--base_name`            |出力ファイル名のヘッダ部分 (無指定の場合は `-i` のファイル名)|