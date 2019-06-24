db.createUser({ user: "portreto", pwd: "portreto", roles: [{ role: "readWrite", db: "auth" }] });
db.createCollection("test", {}) ;