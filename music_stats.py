from collections import namedtuple, Counter
from datetime import datetime, timedelta
import sys
import csv

def print_tops(trackset, time_name):
    top_tracks = Counter([(t.artist, t.title, t.album) for t in trackset]).most_common(10)
    top_artists = Counter([t.artist for t in trackset]).most_common(10)

    print(f"Top tracks {time_name}:")
    for track, count in top_tracks:
        print("{} plays: {} - {} (from {})".format(count, *track))

    print(f"\nTop artists {time_name}:")
    for artist, count in top_artists:
        print(f"{count} plays: {artist}")

def artist_popularity(trackset):
    """ This function calculates artist popularity every year relative
        to the artist's most popular year and taking into account the
        amount of scrobbles every year. """

    artists = set(t.artist for t in trackset)

    artist_pop = {}

    year_counts = Counter(t.date.year for t in trackset)

    for artist in sorted(artists):
        year_counter = Counter([t.date.year for t in trackset if t.artist == artist])

        # get most popular year and amount of songs in that year
        mp_year, mp_count = year_counter.most_common(1)[0]

        artist_pop[artist] = {year:(count*year_counts[mp_year])/(mp_count*year_counts[year])
                              for year,count in year_counter.items()}

    return artist_pop


Track = namedtuple('Track', ['artist', 'album', 'title', 'date'])

r = csv.reader(open(sys.argv[1]))

tracks = [Track(artist, album, title, datetime.strptime(date, "%d %b %Y %H:%M"))
          for artist, album, title, date in r]

tracks.sort(key=lambda track: track.date)

today = datetime.now().date()
last_friday = today - timedelta(days=3+today.weekday())

this_week = [track for track in tracks if track.date.date() >= last_friday]
this_year = [track for track in tracks if track.date >= datetime.strptime("2018", "%Y")]

print(f"# of tracks this week: {len(this_week)}")

print_tops(this_week, "this week")
print()
print_tops(this_year, "this year")

artist_popularity_map = artist_popularity(tracks)

#print("\nRelative artist popularity per year:")
#for artist, years in artist_popularity_map.items():
#    if len(years) == 1: continue # there's not really a trend if the data is 2018: 100%
#    sys.stdout.write(artist + ": ")
#    for year, share in years.items():
#        sys.stdout.write(f"{year}: {100*share}%  ")
#    print()

print("\nArtists you listen to more than last year (excludes single-year artists, and relative to the amount of scrobbles in a year):")
print(', '.join(artist for artist, years in artist_popularity_map.items() if years.get(2018, 0) > years.get(2017, 0) and len(years) > 1))

print("\nArtists you listen to less than last year (same constraints as above):")
print(', '.join(artist for artist, years in artist_popularity_map.items() if years.get(2018, 0) < years.get(2017, 0) and len(years) > 1))
