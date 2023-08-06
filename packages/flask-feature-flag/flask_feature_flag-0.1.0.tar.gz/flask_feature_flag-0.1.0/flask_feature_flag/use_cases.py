from flask import current_app as app
from flask_caching import Cache
from constants_and_utils.constants import responses
from constants_and_utils.constants.enums import HttpCode
from constants_and_utils.utils.use_cases import Response
from constants_and_utils.utils.helpers import recursive_get
from .models import FeatureFlag
from .repository import FeatureRepository


class FeatureResponse(Response):
    """Response for use cases.

    Attributes:
        data (dict): Result.
        http_code (int): Http code.
        message (str): A message.
        errors (list): List of errors.
    """

    def __init__(self, data: dict = None, *args, **Kwargs):
        self.data = data
        super().__init__(*args, **Kwargs)


class GetFeature:
    """Get feature value"""

    def handle(self, feature: str) -> bool:
        """Get feature value according to the type of feature configured.

        Args:
            feature(str): Feature flag name.

        Returns:
            bool: Feature value.
        """
        self.__feature = feature
        return self.__get_feature()

    @property
    def __cache(self):
        """Current cache.

        Returns:
            Cache (flask_caching.Cache): Current cache.
        """
        return Cache(app)

    def __get_feature(self):
        """Call feature method.

        Returns:
            function: function according to the type of feature.
        """
        current_type = app.config.get('FEATURE_FLAG_TYPE')
        type_methods = {
            'FLASK_CONFIG': self.__get_flask_config_feature,
            'MONGO': self.__get_mongo_feature,
        }
        exist = type_methods.get(current_type, None)
        if not exist:
            raise Exception(
                f'feature flag type "{current_type}" does not exist'
                )
        return exist()

    def __get_flask_config_feature(self) -> bool:
        """Get value from flask config.

        Returns:
            bool: Feature value.
        """
        return recursive_get(
            app.config.get('FEATURE_FLAGS'),
            self.__feature,
            default=False
        )

    def __get_mongo_feature(self) -> bool:
        """Get value from the cache or mongo.

        Returns:
            bool: Feature value.
        """
        in_cache = self.__cache.get(self.__feature)
        if not in_cache:
            flag = FeatureRepository.find_one(
                feature_flag=self.__feature
                )
            return True if not flag else flag.feature_flag_value

        return in_cache


class CreateFeatureMongo:
    """Create feature flag in mongo"""

    def handle(self, request: dict) -> Response:
        """
        Args:
            request (dict): Example
                ::
                    {
                        "feature_flag": "feature",
                        "feature_flag_value": true
                    }

        Returns:
            Response: Object Response.
        """
        self._request = request

        valid, response = self.__validate()
        if not valid:
            return response

        self.__save_feature()
        return Response(
            message=responses.CREATED,
            http_code=HttpCode.CREATED
        )

    @property
    def __cache(self):
        """Current cache.

        Returns:
            Cache (flask_caching.Cache): Current cache.
        """
        return Cache(app)

    def __save_feature(self) -> None:
        """Save feature in mongo"""
        flag = FeatureFlag(**self._request)
        flag.save()

        self.__cache.set(
            self._request.get('feature_flag'),
            self._request.get('feature_flag_value')
        )

    def __validate(self) -> (bool, Response):
        """Validations.

        Returns:
            (bool, Reponse): (is_valid, obj of Response with the error)
        """
        valid, errors = self.__request_is_valid()
        if not valid:
            return False, Response(
                message=responses.BAD_REQUEST,
                http_code=HttpCode.BAD_REQUEST,
                errors=errors
            )

        flag = FeatureRepository.find_one(
                feature_flag=self._request.get('feature_flag')
            )
        if flag:
            return False, Response(
                message='FEATURE_ALREADY_EXISTS',
                http_code=HttpCode.FORBIDDEN,
            )

        return True, None

    def __request_is_valid(self) -> (bool, dict):
        """Validate request.

        Returns:
            (bool, dict): if is valid, Structure valid.
        """
        structure = {
            'feature_flag': "<class 'str'>",
            'feature_flag_value': "<class 'bool'>"
        }
        if structure == self.__get_type(self._request):
            return True, None

        return False, structure

    def __get_type(self, value) -> dict:
        """Get dictionary with the class type.

        Returns:
            dict: Dictionary with the class type.
        """
        if isinstance(value, dict):
            return {
                key: self.__get_type(value[key])
                for key in value
                }
        else:
            return str(type(value))


class UpdateFeatureMongo:
    """Update feature flag in mongo"""

    def handle(self, request: dict) -> Response:
        """
        Args:
            request (dict): Example
                ::
                    {
                        "feature_flag": "feature",
                        "feature_flag_value": true
                    }

        Returns:
            Response: Object Response.
        """
        self._request = request

        valid, errors = self.__validate()
        if not valid:
            return Response(
                message=responses.BAD_REQUEST,
                http_code=HttpCode.BAD_REQUEST,
                errors=errors
            )

        return self.__update_feature()

    @property
    def __cache(self):
        """Current cache.

        Returns:
            Cache (flask_caching.Cache): Current cache.
        """
        return Cache(app)

    def __update_feature(self) -> Response:
        """Update feature flag in mongo.

        Returns:
            Response: Object response.
        """
        flag = FeatureRepository.find_one(
                feature_flag=self._request.get('feature_flag')
            )
        if not flag:
            return Response(
                message='FEATURE_FLAG_NOT_FOUND',
                http_code=HttpCode.NOT_FOUND,
            )

        flag.feature_flag_value = self._request.get('feature_flag_value')
        flag.save()

        self.__cache.set(
            self._request.get('feature_flag'),
            self._request.get('feature_flag_value')
        )

        return Response(
            message=responses.OK,
            http_code=HttpCode.OK,
        )

    def __validate(self) -> (bool, dict):
        """Validate request.

        Returns:
            (bool, dict): if is valid, Structure valid.
        """
        structure = {
            'feature_flag': "<class 'str'>",
            'feature_flag_value': "<class 'bool'>"
        }
        if structure == self.__get_type(self._request):
            return True, None

        return False, structure

    def __get_type(self, value) -> dict:
        """Get dictionary with the class type.

        Returns:
            dict: Dictionary with the class type.
        """
        if isinstance(value, dict):
            return {
                key: self.__get_type(value[key])
                for key in value
                }
        else:
            return str(type(value))


class ValidateFeatureMongo:
    """Validate Feature flag in mongo"""

    def handle(self, feature: str) -> FeatureResponse:
        """
        Args:
            feature (str): Feature flag name.

        Returns:
            FeatureResponse: Object response.
        """
        self.__feature = feature
        self.__data = dict()

        self.__validate_in_cache()
        self.__validate_in_mongo()

        return FeatureResponse(
            data=self.__data,
            http_code=HttpCode.OK,
            message=responses.OK
        )

    @property
    def __cache(self) -> Cache:
        """Current cache.

        Returns:
            Cache (flask_caching.Cache): Current cache.
        """
        return Cache(app)

    def __validate_in_cache(self) -> None:
        """Validate if it exists in cache."""

        flag_value = self.__cache.get(self.__feature)
        if not flag_value:
            self.__data.update({'cache': False})
        else:
            self.__data.update({'cache': flag_value})

    def __validate_in_mongo(self) -> None:
        """Validate if it exists in mongo."""

        flag = FeatureRepository.find_one(
            feature_flag=self.__feature
            )

        if not flag:
            self.__data.update({'mongo': False})
        else:
            self.__data.update({'mongo': flag.feature_flag_value})


class DeleteFeatureMongo:

    def handle(self, feature: str) -> Response:
        """
        Args:
            feature (str): Feature flag name.

        Returns:
            Response: Object response.
        """
        self.__feature = feature

        self.__delete_in_cache()
        self.__delete_in_mongo()

        return Response(
            http_code=HttpCode.OK,
            message=responses.OK
        )

    @property
    def __cache(self):
        """Current cache.

        Returns:
            Cache (flask_caching.Cache): Current cache.
        """
        return Cache(app)

    def __delete_in_cache(self) -> None:
        """Delete feature in cache"""
        self.__cache.delete(self.__feature)

    def __delete_in_mongo(self) -> None:
        """Delete feature in mongo"""
        flag = FeatureRepository.find_one(
            feature_flag=self.__feature
        )
        if flag:
            flag.delete()
