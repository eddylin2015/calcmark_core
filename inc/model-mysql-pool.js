'use strict';
const mysql = require('mysql');
const mysqlcfg = require('../../mysql250/mysql250config');
const pool = mysqlcfg.esdbPool;


async function DB_reader(sql, params = []) {
    let res_set = null
    return new Promise((resolve, reject) => {
        pool.getConnection(async function (err, connection) {
            if (err) { cb(err); return; }
            res_set = await new Promise((resolve, reject) => {
                connection.query(sql, params, (err, result) => {
                    if (err) { console.log(err); reject(err); }
                    resolve(result);
                });
            });
            resolve(res_set)
            connection.release();
        });
    });
}


function DataReaderQuery(sql, params,cb) {
    pool.getConnection(function (err, conn) {
        if (err) { cb(err); return; }
        conn.query(
            sql,
            params,
            (err, results) => {
                if (err) {
                    cb(err);
                    return;
                }
                cb(null, results);
                conn.release();
            });
    });
}
module.exports = {
    DataReaderQuery: DataReaderQuery,
    DB_reader: DB_reader,
};

if (module === require.main) {
    const prompt = require('prompt');
    prompt.start();
    console.log(
        `Running this script directly will allow you to initialize your mysql
    database.\n This script will not modify any existing tables.\n`);
    prompt.get(['user', 'password'], (err, result) => {
        if (err) {
            return;
        }
        createSchema(result);
    });
}
