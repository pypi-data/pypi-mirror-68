from mirroring_flickr.parser import get_arguments
from mirroring_flickr.flickr import FlickrUserPhotostreamMirroringAgent
import mirroring_flickr.constants as constants


def main():
    """Entry point"""
    name_space = get_arguments()
    mirroring_agent = FlickrUserPhotostreamMirroringAgent(
        name_space.username,
        name_space.consumer_key,
        name_space.consumer_secret,
        name_space.cache_path,
        name_space.cache_directory_depth,
        name_space.image_only,
        name_space.info_level,
        name_space.info_only,
        name_space.cache_strategy)
    mirroring_agent.run()
    constants.SESSION.close()


if __name__ == "__main__":
    main()
