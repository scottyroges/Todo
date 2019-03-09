const AmazonCognitoIdentity = require('amazon-cognito-identity-js');
const CognitoUserPool = AmazonCognitoIdentity.CognitoUserPool;
const AWS = require('aws-sdk');
const request = require('request');
const jwkToPem = require('jwk-to-pem');
const jwt = require('jsonwebtoken');
global.fetch = require('node-fetch');
global.navigator = {userAgent: "node"}

const poolData = {
    UserPoolId: "us-east-2_GgKNcQC1D", // Your user pool id here    
    ClientId: "ok1ovqmqrnc60jt8fi4egtm31" // Your client id here
};
const pool_region = 'us-east-1';
const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

function createUser(email, username, password) {
    var dataEmail = {
        Name: 'email',
        Value: email
    };

    var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(dataEmail);
    attributeList = [];
    attributeList.push(attributeEmail);

    userPool.signUp(username, password, attributeList, null, function(err, result) {
        if (err) {
            console.log(err);
            return;
        }
        cognitoUser = result.user;
        console.log('user name is ' + cognitoUser.getUsername());
    });
}

function login(username, password) {
    var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails({
        Username : username,
        Password : password,
    });

    var userData = {
        Username : username,
        Pool : userPool
    };
    var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
    console.log(JSON.stringify(cognitoUser))
    console.log(JSON.stringify(authenticationDetails))
    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function (result) {
            console.log('access token: ' + result.getAccessToken().getJwtToken());
            console.log('id token: ' + result.getIdToken().getJwtToken());
            console.log('refresh token: ' + result.getRefreshToken().getToken());
        },
        onFailure: function(err) {
            console.log(err);
        },

    });
}

// createUser("srogener+admin@gmail.com", "admin_scott", "!Test123")
// login("admin_scott", "!Test123")
login("scottyroges", "!Fucker1")