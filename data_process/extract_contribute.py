# -*- coding:utf-8 -*-
"""
提取贡献度特征
"""
import pymongo
import pandas as pd
import random

movie = pd.read_csv('../input/movie_raw.csv')

cast_portrait = pymongo.MongoClient('192.168.200.47', 27017)['Land_Movie']['cast_personas']

result = []
for index, item in movie.iterrows():
    print(index)
    c = dict()
    movie_id = item['movie_id']
    movie_name = item['movie_name']
    schedule_rate = item['schedule_rate']
    want_count = item['want_count']
    score = item['score']

    c['movie_id'] = movie_id
    c['movie_name'] = movie_name
    c['schedule_rate'] = schedule_rate
    c['want_count'] = want_count
    c['score'] = score

    is_give_up = False
    try:
        director = item['director'].split('/')[0]
    except:
        continue
    cursor = cast_portrait.find({'name': director})
    if cursor.count() > 0:
        doc = cursor[0]
        director_name = doc['name']
        print(director_name)
        director_influence = doc['influence']
        director_award_count = doc['award_count']
        # director_weibo_pos = doc['weibo_pos']
        director_num_follow = doc['average_follow_count']
        # director_num_tweets = doc['average_reports_count']
        director_num_fan = doc['average_followers_count']
        director_average_attitudes_count = doc['average_attitudes_count']
        try:
            director_overall = doc['director_overall']
        except KeyError:
            director_overall = random.uniform(3, 4.5)
        director_average_comments_count = doc['average_comments_count']
        director_average_reports_count = doc['average_reports_count']
        try:
            character = doc['character']
        except KeyError:
            character = random.uniform(3, 4.5)
        try:
            movie_pace = doc['movie_pace']
        except KeyError:
            movie_pace = random.uniform(3.0, 4.5)
        c['director_name'] = director_name
        c['director_influence'] = director_influence
        c['director_award_count'] = director_award_count
        # c['director_weibo_pos'] = director_weibo_pos
        c['director_num_follow'] = director_num_follow
        # c['director_num_tweets'] = director_num_tweets
        c['director_num_fan'] = director_num_fan
        c['director_overall'] = director_overall
        # c['director_average_attitudes_count'] = director_average_attitudes_count
        # c['director_average_followers_count'] = director_num_fan
        c['director_average_reports_count'] = director_average_reports_count
        c['director_average_attitudes_count'] = director_average_attitudes_count
        c['director_average_comments_count'] = director_average_comments_count
        c['character'] = character
        c['movie_pace'] = movie_pace
    else:
        continue

    try:
        actors = item['actors'].split(',')
    except:
        continue
    if len(actors) < 4:
        continue

    for i in range(4):
        try:
            print(actors[i])
            doc = cast_portrait.find({'name': actors[i].strip()})[0]
        except:
            is_give_up = True
            break
        actor_name = doc['name']
        actor_influence = doc['influence']
        actor_award_count = doc['award_count']
        # actor_weibo_pos = doc['weibo_pos']
        actor_num_follow = doc['average_follow_count']
        # actor_num_tweets = doc['average_reports_count']
        actor_num_fan = doc['average_followers_count']
        actor_average_comments_count = doc['average_comments_count']
        actor_average_reports_count = doc['average_reports_count']
        actor_average_attitudes_count = doc['average_attitudes_count']
        try:
            figure = doc['figure']
        except KeyError:
            figure = random.uniform(3, 4.5)
        try:
            actor_overall = doc['actor_overall']
        except KeyError:
            actor_overall = random.uniform(3, 4.5)
        try:
            temperament = doc['temperament']
        except KeyError:
            temperament = random.uniform(3, 4.5)
        try:
            voice = doc['voice']
        except KeyError:
            voice = random.uniform(3, 4.5)
        try:
            line_ability = doc['line_ability']
        except KeyError:
            line_ability = random.uniform(3, 4.5)
        try:
            acting = doc['acting']
        except KeyError:
            acting = random.uniform(3, 4.5)
        try:
            appearance = doc['appearance']
        except KeyError:
            appearance = random.uniform(3, 4.5)
        c['actor' + str(i + 1) + '_name'] = actor_name
        c['actor' + str(i + 1) + '_influence'] = actor_influence
        c['actor' + str(i + 1) + '_award_count'] = actor_award_count
        # c['actor' + str(i) + '_weibo_pos'] = actor_award_count
        # c['actor' + str(i) + '_num_follow'] = actor_weibo_pos
        # c['actor' + str(i) + '_num_tweets'] = actor_num_tweets
        c['actor' + str(i + 1) + '_actor_average_comments_count'] = actor_average_attitudes_count
        c['actor' + str(i + 1) + '_actor_average_reports_count'] = actor_average_reports_count
        c['actor' + str(i + 1) + '_actor_average_attitudes_count'] = actor_average_attitudes_count
        c['actor' + str(i + 1) + '_num_fans'] = actor_num_fan
        c['actor' + str(i + 1) + '_figure'] = figure
        c['actor' + str(i + 1) + '_overall'] = actor_overall
        c['actor' + str(i + 1) + '_voice'] = voice
        c['actor' + str(i + 1) + '_line_ability'] = line_ability
        c['actor' + str(i + 1) + '_acting'] = acting
        c['actor' + str(i + 1) + '_appearance'] = appearance

    if is_give_up:
        # print(c)
        continue
    # print(c)
    result.append(c)

df = pd.DataFrame(result, columns=['movie_id', 'movie_name', 'schedule_rate', 'want_count', 'score', 'director_name',
                                   'director_influence', 'director_award_count', 'director_num_follow',
                                   'director_num_fan', 'director_overall', 'director_average_reports_count',
                                   'director_average_comments_count', 'director_average_attitudes_count',
                                   'actor1_name', 'actor1_average_comments_count', 'actor1_average_reports_count',
                                   'actor1_average_attitudes_count', 'actor1_figure', 'actor1_overall', 'actor1_voice',
                                   'actor1_influence', 'actor1_line_ability', 'actor1_acting', 'actor1_appearance',
                                   'actor1_award_count', 'actor1_num_follow',
                                   'actor1_num_fans', 'actor2_name', 'actor2_influence',
                                   'actor2_voice', 'actor2_line_ability', 'actor2_acting', 'actor2_appearance',
                                   'actor2_average_comments_count', 'actor2_average_reports_count',
                                   'actor2_average_attitudes_count', 'actor2_figure', 'actor2_overall',
                                   'actor2_num_follow',
                                   'actor2_num_fans', 'actor3_name', 'actor3_influence', 'actor3_award_count',
                                   'actor3_overall', 'actor3_voice', 'actor3_acting', 'actor3_appearance',
                                   'actor3_average_comments_count', 'actor3_average_reports_count', 'actor3_figure',
                                   'actor3_num_follow', 'actor3_average_attitudes_count',
                                   'actor3_num_fans', 'actor3_line_ability',
                                   'actor4_name', 'actor4_influence', 'actor4_acting', 'actor4_appearance',
                                   'actor4_award_count',
                                   'actor4_average_comments_count', 'actor4_average_reports_count', 'actor4_overall',
                                   'actor4_num_follow', 'actor4_voice', 'actor4_line_ability',
                                   'actor4_num_fans', 'actor4_figure',
                                   'actor4_average_attitudes_count'])

df.to_csv('../input/contribute_feature.csv', index=False, encoding='utf-8')
