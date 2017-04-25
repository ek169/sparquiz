import random, hashlib, hmac, string

def make_salt():
    return ''.join(random.choice(string.letters) for x in range(10))

def make_pw_hash(user, pw, salt = None):

    if not salt:
        salt = make_salt()

    hash = hashlib.sha256(user + pw + salt).hexdigest()
    print(hash, salt)
    return '%s,%s' % (hash, salt)

def validate_pw(user, pw, hash):
    salt = hash.split(',')[1]
    return hash == make_pw_hash(user, pw, salt)

def hash_cookie(s):
    secret = 'THISISASECRET'
    return hmac.new(secret, s).hexdigest()

def make_secure_cookie(user_id):
    return '%s|%s' % (user_id, hash_cookie(user_id))

def validate_cookie(t):
    user_id = t.split('|')[0]
    if t == make_secure_cookie(user_id):
        return user_id




