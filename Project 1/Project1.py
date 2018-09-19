# Mojo box Office data
from urllib.request import urlopen


# the number of pages need to be updated to reflect the current total pages
num_pages = 8
movies_per_page = 100

# the file in which we want o save Movie Name, Movie ID and Studio that produced movies
out_file = open('mojo_data.csv', 'w')

# the url we need to locate the movies names
# sorted in reverse chronological order
url = 'https://www.boxofficemojo.com/yearly/chart/?page={start_number}&view=releasedate&view2=domestic&yr=2017&p=.htm'

# the string pattern to locate some relevant information
MovieID_start_pattern = '<a href="/movies/?id='
MovieID_end_pattern =  '.htm">'

MovieName_start_pattern = '.htm>'
MovieName_end_pattern = '</a>'

Studio_start_pattern = '<a href="/studio/chart/?studio='
Studio_end_pattern = '.htm>'

Movie_count = 0

# put the header to the file
out_file.write('MovieID,MovieName,Studio' + '\n')
MovieID = 0

for page in range(num_pages):

    print('processing page', page)

    # open the url and save the source code string to page_content
    html = urlopen(url.format(start_number=page * movies_per_page))
    page_content = html.read().decode('utf-8')
    #print(page_content)

    # locate the beginning of an individual movie
    Studio = page_content.find(Studio_start_pattern)
    print("Studio start" , Studio)

    while Studio != -1:
        # it means there at least one more movie to be crawled
        Movie_count += 1

        # get the MovieName
        cut_front = page_content.find(
            MovieName_start_pattern, Studio) + len(MovieName_start_pattern)
        cut_end = page_content.find(MovieName_end_pattern, cut_front)
        MovieName = page_content[cut_front:cut_end]
        MovieName = MovieName.strip()  # remove white spaces around
        print(MovieName)

        # get the MovieID
        cut_front = page_content.find(
            MovieID_start_pattern, cut_end) + len(MovieID_start_pattern)
        cut_end = page_content.find(MovieID_end_pattern, cut_front)
        MovieID = page_content[cut_front:cut_end]
        MovieID = MovieID.strip()  # remove white spaces around
        print(MovieID)

        # save the data into out_file
        #MovieID += 1
        out_file.write(','.join([str(MovieID), MovieName, Studio]) + '\n')
        Studio_start = page_content.find(Studio_start_pattern, cut_end)

    print('crawled', Movie_count, 'Movies so far')

print("Program finished!")

out_file.close()


