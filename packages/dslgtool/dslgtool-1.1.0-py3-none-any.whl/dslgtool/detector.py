from spriteutil_final.spriteutil import SpriteSheet
from PIL import Image
import exifread
import math


def load_image_and_correct_orientation(image_file_path):
    """Rotate image to the correct orientation

    Arguments:
        image_file_path {str} -- path name of image file

    Returns:
        Image -- image with the correct orientation
    """
    image = Image.open(image_file_path)
    tags = {}

    with open(image_file_path, 'rb') as f:
        # Read the information of image
        tags = exifread.process_file(f, details=False)

    # If the information contains image orientation detail
    if "Image Orientation" in tags.keys():
        orientation = tags["Image Orientation"]
        val = orientation.values
        # Rotate image to the right orientation
        if 3 in val:
            image = image.transpose(Image.ROTATE_180)
        if 6 in val:
            image = image.transpose(Image.ROTATE_270)
        if 8 in val:
            image = image.transpose(Image.ROTATE_90)
    return image


def calculate_brightness(image):
    """Calculate brightness of image based on histogram

    Arguments:
        image {Image} -- An Image object

    Returns:
        float -- Brightness of image, from 0.0 to 1.0
    """
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale


def monochromize_image(image, brightness=None):
    """Convert image into monochrome with only black and white

    Arguments:
        image {Image} -- Image to convert

    Keyword Arguments:
        brightness {float} -- Brightness of image(optional) (default: {None})

    Returns:
        Image -- Monochromized image
    """
    if not brightness:
        brightness = calculate_brightness(image)

    # Use threshold to check if a pixel is considered black or white
    threshold = brightness * 255
    monochrome_image = image.convert('L')
    pix_list = monochrome_image.load()
    width, height = monochrome_image.size

    for x in range(width):
        for y in range(height):

            if pix_list[x, y] < threshold:
                pix_list[x, y] = 0
            else:
                pix_list[x, y] = 255

    return monochrome_image


def check_difference(ratio, threshold):
    return 1 - threshold < ratio < 1 + threshold


def filter_visible_sprites(sprites, min_surface_area):
    """Filter visible sprites based on min surface area

    Arguments:
        sprites {list} -- List of all sprite objects
        min_surface_area {int} -- Minnimum surface area to compare, range from 0.0 to 1.0

    Returns:
        list -- List of visible sprites
    """
    visible_sprites = []

    for sprite in sprites:
        if sprite.width * sprite.height >= min_surface_area:
            visible_sprites.append(sprite)

    return visible_sprites


def filter_square_sprites(sprites, similarity_threshold):
    """Filter square sprites based on similarity threshold

    Arguments:
        sprites {list} -- List of all sprite objects
        similarity_threshold {float} -- Maximum threshold to compare, range from 0.0 to 1.0

    Returns:
        list -- List of square sprites
    """
    square_sprites = []

    for sprite in sprites:
        if check_difference(sprite.width / sprite.height, similarity_threshold):
            square_sprites.append(sprite)

    return square_sprites


def filter_dense_sprites(sprites, density_threshold):
    """Filter dense sprites based on density threshold

    Arguments:
        sprites {list} -- List of all sprite objects
        density_threshold {float} -- Minimum threshold to compare, range from 0.0 to 1.0

    Returns:
        list -- List of dense sprites
    """
    dense_sprites = []

    for sprite in sprites:
        surface_area = sprite.width * sprite.height

        if sprite.total_pixel / surface_area > density_threshold:
            dense_sprites.append(sprite)

    return dense_sprites


def group_sprites_by_similar_size(sprites, similar_size_threshold):
    """Divide list of sprites into lists which contain similar size sprite

    Arguments:
        sprites {list} -- list of Sprite objects
        similar_size_threshold {float} -- A float number to check if 2 sprites have similar size

    Returns:
        list -- A list contains smallers lists in which all sprites have similar size
    """
    group_sizes = {}

    for sprite in sprites:

        sprite_area = sprite.width * sprite.height
        in_group = False

        # Check if sprite's size is similar to any size in group_sizes
        for size in group_sizes.keys():

            # If yes, add sprite to this group
            if check_difference(sprite_area / size, similar_size_threshold):
                group_sizes[size].append(sprite)
                in_group = True
                break

        # If sprite's size doesn't exist in group_sizes, create new key
        if not in_group:
            group_sizes[sprite_area] = [sprite]

    return [group_sizes[size] for size in group_sizes.keys() if len(group_sizes[size]) >= 3]


def calculate_distance(x1, y1, x2, y2):
    """Calculate distance between 2 points

    Returns:
        float -- calcualted distance
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def group_sprites_by_similar_distance(sprites, similar_distance_threshold):
    """Devide list of sprites into groups in which all tuple of sprites have similar distance

    Arguments:
        sprites {list} -- List of sprites
        similar_distance_threshold {float} -- A float number represent the difference between 2
                                             distance, below which 2 distances are considered similar

    Returns:
        list -- List of all groups in which all sprite tuples have similar distance
    """
    group_distance = {}

    for x in range(len(sprites) - 1):
        # Check distance between each sprite and all other sprites
        cur_sprite = sprites[x]
        x1, y1 = cur_sprite.center

        for y in range(x + 1, len(sprites)):

            check_sprite = sprites[y]
            x2, y2 = check_sprite.center
            cur_distance = calculate_distance(x1, y1, x2, y2)
            in_group = False

            # Check if the calculated distance is similar to any distance in group_distance
            for distance in group_distance.keys():

                # If yes, add this tuple of sprites to the list
                if check_difference(cur_distance / distance, similar_distance_threshold):
                    in_group = True
                    group_distance[distance].append((cur_sprite, check_sprite))
                    break

            # If the calculated distance is not in group_distance, create new key
            if not in_group:
                group_distance[cur_distance] = [(cur_sprite, check_sprite)]

    return [group_distance[dist] for dist in group_distance.keys() if len(group_distance[dist]) >= 2]


def group_sprites_by_similar_size_and_distance(sprites, similar_size_threshold, similar_distance_threshold):
    """Divide list of sprites into smaller groups which contain sprites that have similar size and distance

    Arguments:
        sprites {list} -- List of sprites
        similar_size_threshold {float} -- A float number represent the difference between size of 2 sprites, 
        below which 2 sprites are cosidered having similar size
        similar_distance_threshold {float} -- A float number represent the difference between 2 distances,
        below which 2 distances are considered similar to each other.

    Returns:
        list -- List of all groups that contains tuples of similar size and distance sprites.
    """
    group_sizes = group_sprites_by_similar_size(
        sprites, similar_size_threshold)

    group_distance = []

    for group in group_sizes:
        group_distance.extend(group_sprites_by_similar_distance(
            group, similar_distance_threshold))

    return group_distance


def combine_sprite_pair(pair_1, pair_2):
    """Combine 2 tuples of of sprite pairs into one by finding the common sprite
    
    Arguments:
        pair_1, pair_2 {tuple} -- Tuple contains 2 sprite
    
    Returns:
        tuple or None -- If 2 tuple can be combined, this function will return the tuple which contains 3 sprites, otherwise None
    """
    combined_tuple = None
    set_1 = set(pair_1)
    set_2 = set(pair_2)

    diff_set = set_2 - set_1

    # If there is one commone sprite between 2 tuples
    if len(diff_set) == 1:
        common_set = set_2 - diff_set
        first_sprite = (set_1 - common_set).pop()
        last_sprite = diff_set.pop()
        common_sprite = common_set.pop()
        combined_tuple = (first_sprite, common_sprite, last_sprite)

    return combined_tuple


def check_angle(sprites_tuple, orthogonality_threshold):
    """Check if the angle between 3 sprites forms a right angle
    
    Arguments:
        sprites_tuple {tuple} -- Tuple contains 3 sprite, common sprite must have index 1
        orthogonality_threshold {float} -- A float number represent the difference between the calculated angle between
        3 sprites and 90, below which that angle will be considered to be the right angle
    
    Returns:
        tuple or None -- If 3 sprites form a right angle, this function will return a tuple contains 3 sprites
        in order (top_left_sprite, top_right_sprite, bottom_left_sprite), None ortherwise
    """
    if not sprites_tuple:
        return None

    bottom_left_sprite, top_left_sprite, top_right_sprite = sprites_tuple
    x1, y1 = bottom_left_sprite.center
    x2, y2 = top_left_sprite.center
    x3, y3 = top_right_sprite.center

    angle = math.degrees(math.atan2(y3 - y2, x3-x2) - math.atan2(
            y1 - y2, x1 - x2))

    if angle < 0:
        bottom_left_sprite, top_right_sprite = top_right_sprite, bottom_left_sprite
        angle = -angle

    if check_difference(angle / 90, orthogonality_threshold):
        return(top_left_sprite, top_right_sprite, bottom_left_sprite)
    else:
        return None
    

def search_position_detection_patterns(sprite_pairs, orthogonality_threshold):
    """Find all position detection patterns by listing all tuple contains 3 sprites that form a right angle
    
    Arguments:
        sprite_pairs {list} --List of all sprite pair that are similar in size and distance
        orthogonality_threshold {float} -- A float number represent the difference between the calculated angle between
        3 sprites and 90, below which that angle will be considered to be the right angle
    
    Returns:
        list -- List of all tuples contain 3 sprites that form a sprite angle
    """
    group_patterns = []

    for x in range(len(sprite_pairs) - 1):
        cur_pair = sprite_pairs[x]

        for y in range(x + 1, len(sprite_pairs)):
            check_pair = sprite_pairs[y]

            # Combine 2 tuple into one by merging the common sprite
            combined_tuple = combine_sprite_pair(cur_pair, check_pair)
            # Check if the combined tuple is of the right angle
            tuple_pattern = check_angle(combined_tuple, orthogonality_threshold)
            if tuple_pattern:
                group_patterns.append(tuple_pattern)

    return group_patterns


def find_right_angle_from_group_size_and_distance(list_pairs, orthogonality_threshold):
    """Find all tuple containing 3 sprites that form a right angle from the list containing similar size and distance sprite groups
    
    Arguments:
        list_pairs {list} -- List of all groups containing similar size and distance spritea
        orthogonality_threshold {float} -- A float number represent the difference between the calculated angle between
        3 sprites and 90, below which that angle will be considered to be the right angle
    
    Returns:
        list -- List of all tuples contain 3 sprites that form a sprite angle
    """
    group_right_angle = []

    for sprite_pairs in list_pairs:
        group_right_angle.extend(search_position_detection_patterns(sprite_pairs, orthogonality_threshold))

    return group_right_angle


def is_outer_bounding_box(sprite_outer, sprite_inner):
    """Check if a sprite is outer of another sprite
    
    Arguments:
        sprite_outer {Sprite} -- Outer sprite object
        sprite_inner {Sprite} -- Inner sprite object
    
    Returns:
        boolean -- True if the outer sprite covers the inner sprite, False otherwise
    """
    top_out, left_out = sprite_outer.top_left 
    bottom_out, right_out = sprite_outer.bottom_right

    top_in, left_in = sprite_inner.top_left
    bottom_in, right_in = sprite_inner.bottom_right

    if all(left_out < x < right_out for x in (left_in, right_in)) and\
        all(top_out < x < bottom_out for x in (top_in, bottom_in)):
        return True 

    return False


def get_outer_pattern(group_1, group_2):
    """Find the outer pair of 2 sprite pairs
    
    Arguments:
        group_1 {tuple} -- Group Sprite 1
        group_2 {tuple} -- Group Sprite 2
    
    Returns:
        tuple or None -- The tuple of the outer group, None if no tuple contains another tuple
    """
    surface_area_1 = group_1[0].width * group_1[0].height
    surface_area_2 = group_2[0].width * group_2[0].height

    if surface_area_1 < surface_area_2:
        big_group = group_2
        small_group = group_1
    else:
        big_group = group_1
        small_group = group_2

    for x in range(len(big_group)):
        if not is_outer_bounding_box(big_group[x], small_group[x]):
            return None 

    return big_group


def filter_matching_inner_outer_finder_patterns(finder_patterns):
    """Filter all outer finder patterns from list of all finder_patterns
    
    Arguments:
        finder_patterns {list} -- List of all finder patterns
    
    Returns:
        list -- List of all outer patterns found
    """
    outer_finder_patterns = []

    for x in range(len(finder_patterns) - 1):
        cur_group = finder_patterns[x]

        for y in range(x + 1, len(finder_patterns)):
            check_group = finder_patterns[y]

            outer_pattern = get_outer_pattern(cur_group, check_group)
            if outer_pattern:
                outer_finder_patterns.append(outer_pattern)

    return outer_finder_patterns


def is_containing_qr_code(img_path):
    import time

    start = time.time()

    image = load_image_and_correct_orientation(img_path)

    gray_image = monochromize_image(image, calculate_brightness(image))
    print(gray_image.size)

    demo = SpriteSheet(gray_image, 255)

    sprites, _ = demo.find_sprites()

    sprites = sprites.values()

    visible_sprites = filter_visible_sprites(sprites, 1500)
    print(len(visible_sprites), '-'*10, 'visible_sprites')

    square_sprites = filter_square_sprites(visible_sprites, 0.3)
    print(len(square_sprites), '-'*10, 'square_sprites')

    dense_sprites = filter_dense_sprites(square_sprites, 0.2)
    print(len(dense_sprites), '-'*10, 'dense_sprites')

    print(time.time() - start)

    start = time.time()
    a = group_sprites_by_similar_size_and_distance(dense_sprites, 0.4, 0.4)
    print(len(a))
    b = find_right_angle_from_group_size_and_distance(a, 0.4)
    demo.make_sprite_border_image(dense_sprites).save('1.png')
    print(len(b))
    print(time.time() - start)

    start = time.time()
    c = filter_matching_inner_outer_finder_patterns(b)
    print(time.time() - start)
    print(len(c))
    if c:
        return True 
    return False