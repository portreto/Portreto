db.createUser({ user: "portreto", pwd: "portreto", roles: [{ role: "readWrite", db: "appdata" }] });
db.createCollection("test", {}) ;