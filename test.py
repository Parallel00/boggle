from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(sl):
        sl.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(sf):
        with sf.client:
            response = sf.client.get('/')
            sf.assertIn('board', session)
            sf.assertIsNone(session.get('highscore'))
            sf.assertIsNone(session.get('nplays'))
            sf.assertIn(b'<p>High Score:', response.data)
            sf.assertIn(b'Score:', response.data)
            sf.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(dw):
        with dw.client as clt:
            with clt.session_transaction() as ltrs:
                ltrs['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = dw.client.get('/check-word?word=cat')
        dw.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(slf):
        slf.client.get('/')
        response = slf.client.get('/check-word?word=impossible')
        slf.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(slf):
        slf.client.get('/')
        response = slf.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        slf.assertEqual(response.json['result'], 'not-word')

