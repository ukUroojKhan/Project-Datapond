from rest_framework import serializers
from django.contrib.auth.models import User
from assets.jwt_utility import JWTUtility
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from user_auth.models import Session

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'username': {'min_length': 4}, 'first_name': {'min_length': 3}, 'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value    

class UserLoginSerializer(UserSerializer):
    
    token = serializers.SerializerMethodField()
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('token',)

    def get_token(self, user):
        token_Gen=JWTUtility.encode_token(user)
        return token_Gen

class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = ('id','user_id','token')

class clientSerializer(serializers.Serializer):
    email = serializers.CharField()
    class Meta:
        fields = ['email']

class SaveFileDBSerializer(serializers.Serializer):
    DataType = serializers.CharField()
    class Meta:
        fields = ['DataFile', 'DataType']

class ApisSerializer(serializers.Serializer):
    apis_url = serializers.CharField()
    class Meta:
        fields = ['apis_url']

class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    class Meta:
        fields = ['file_uploaded']

class firebaseSerializer(serializers.Serializer):
    firebase_url = serializers.CharField()
    firebase_table = serializers.CharField()
    firebase_cred = serializers.FileField()
    class Meta:
        fields = ['firebase_url','firebase_table','firebase_cred']

class gitprivateSerializer(serializers.Serializer):
    git_username = serializers.CharField()
    git_token = serializers.CharField()
    git_url = serializers.CharField()
    class Meta:
        fields = ['git_username', 'git_token', 'git_url']

class gitpublicSerializer(serializers.Serializer):
    git_puburl = serializers.CharField()
    class Meta:
        fields = ['git_puburl']

class mariadbSerializer(serializers.Serializer):
    maria_host = serializers.CharField()
    maria_user = serializers.CharField()
    maria_db = serializers.CharField()
    maria_table = serializers.CharField()
    maria_pass = serializers.CharField(style={'input_type': 'password'})
    class Meta:
        fields = ['maria_host', 'maria_user', 'maria_pass', 'maria_db', 'maria_table']

class mongodbSerializer(serializers.Serializer):
    mongo_client = serializers.CharField()
    mongo_db = serializers.CharField()
    mongo_collection = serializers.CharField()
    class Meta:
        fields = ['mongo_client', 'mongo_db','mongo_collection']

class MSsqlSerializer(serializers.Serializer):
    MSsql_Driver = serializers.CharField()
    MSsql_server = serializers.CharField()
    MSsql_db = serializers.CharField()
    MSsql_table = serializers.CharField()
    class Meta:
        fields = ['MSsql_Driver', 'MSsql_server', 'MSsql_db', 'MSsql_table']

class mysqlSerializer(serializers.Serializer):
    mysql_host = serializers.CharField()
    mysql_user = serializers.CharField()
    mysql_db = serializers.CharField()
    mysql_table = serializers.CharField()
    mysql_pass = serializers.CharField(style={'input_type': 'password'})
    class Meta:
        fields = ['mysql_host', 'mysql_user', 'mysql_db', 'mysql_table', 'mysql_pass']

class postgresSerializer(serializers.Serializer):
    psql_host = serializers.CharField()
    psql_user = serializers.CharField()
    psql_db = serializers.CharField()
    psql_table = serializers.CharField()
    psql_pass = serializers.CharField(style={'input_type': 'password'})
    class Meta:
        fields = ['psql_host', 'psql_user', 'psql_db', 'psql_table', 'psql_pass']

class SQLiteSerializer(serializers.Serializer):
    sqlite_table = serializers.CharField()
    sqlite_file = serializers.FileField()
    class Meta:
        fields = ['sqlite_table', 'sqlite_file']

class DatatypeSerializer(serializers.Serializer):
    data_type = serializers.CharField()
    selected_column = serializers.CharField()
    class Meta:
        fields = ['file_uploaded', 'data_type', 'selected_column']

class ColumnEditSerializer(serializers.Serializer):
    column_edit = serializers.CharField()
    class Meta:
        fields = ['file_path', 'column_edit']

class ColumnFiltersSerializer(serializers.Serializer):
    test_file = serializers.FileField()
    column_filter = serializers.CharField()
    class Meta:
        fields = ['column_filter', 'test_file']

class ConcatUploadSerializer(serializers.Serializer):
    file_uploaded2 = serializers.FileField()
    axis = serializers.CharField()
    class Meta:
        fields = ['file_uploaded2', 'axis']

class MergeUploadSerializer(serializers.Serializer):
    left_on_col = serializers.CharField()
    right_on_col = serializers.CharField()
    how = serializers.CharField()
    suffixes_x = serializers.CharField()
    suffixes_y = serializers.CharField()
    class Meta:
        fields = ['left_on_col', 'right_on_col','how', 'suffixes_x', 'suffixes_y']

class aggregateSerializer(serializers.Serializer):
    agg_col = serializers.CharField()
    agg_value = serializers.CharField()
    class Meta:
        fields = ['agg_file', 'agg_col', 'agg_value']

class visualizeSerializer(serializers.Serializer):
    visualize_col1 = serializers.CharField()
    visualize_col2 = serializers.CharField()
    class Meta:
        fields = ['visualize_col1', 'visualize_col2']
