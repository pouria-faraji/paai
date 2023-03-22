// Connection url = mongodb://paaiAdmin:paaiAdminPasswd%2123@localhost:27017/paai?authSource=paai
db.createUser(
    {
        user: "paaiAdmin",
        pwd: "paaiAdminPasswd!23",
        roles: [
            {
                role: "readWrite",
                db: "paai"
            }
        ]
    }
);