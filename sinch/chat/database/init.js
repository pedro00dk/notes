/*
 * Initialization script for the mongo database.
 *
 * The init script uses environment variables to set up user accounts and collections for a given database.
 */

/**
 * The database to set up accounts and collections.
 * If not provided, the default `test` database is used.
 *
 * @type {string}
 */
const database = _getEnv('MONGO_INITDB_DATABASE') || 'test'

/**
 * List of users to create.
 *
 * Each user is an object with containing a user `name` and a password (`pwd`).
 * All users are create with `readWrite` permissions for `database`.
 *
 * @type {{user: string, pwd: string}[]}
 */
const users = JSON.parse(_getEnv('MONGO_USERS') || '[]')

/**
 * List of collections to create in `database`.
 *
 * @type {string[]}
 */
const collections = JSON.parse(_getEnv('MONGO_COLLECTIONS') || '[]')

users.forEach(({ user, pwd }) => db.createUser({ user, pwd, roles: [{ role: 'readWrite', db: database }] }))
collections.forEach(collection => db.getSiblingDB(database).createCollection(collection))
