#!/usr/bin/env python3


from flickr_pkg.flickr import CachingStrategy
from flickr_pkg.flickr import get_arguments

from flickr_pkg.flickr import FlickrUserPhotostreamMirroringAgent


def main():
    # DEMO WP13

    # mirroring_agent=FlickrUserPhotostreamMirroringAgent(
    #     'manhhai',
    #     '861fa02399dd83d930fac3375c48de7b',
    #     '16b0f2e61a0a8bb6')

    # flickr_api=FlickrApi(
    #     '861fa02399dd83d930fac3375c48de7b', '16b0f2e61a0a8bb6')
    # photo=FlickrPhoto('49674775373', Label(
    #     'Huế 1920-1929 - Chez un grand mandarin : avant le repas', Locale('fra')))

    #Demo WP14
    console_object = vars(get_arguments())
    catching_stategy = CachingStrategy.FIFO

    if console_object['lifo']:
        catching_stategy = CachingStrategy.LIFO
    if console_object['fifo']:
        catching_stategy = CachingStrategy.FIFO

    mirroring_agent = FlickrUserPhotostreamMirroringAgent(
        console_object['username'],
        console_object['consumer_key'],
        console_object['consumer_secret'],
        caching_strategy = catching_stategy,
        image_only = console_object['image_only'],
        info_only = console_object['info_only'],
        info_level = console_object['LEVEL']

    )

    mirroring_agent.run()


if __name__ == "__main__":
    main()
