from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User

# _() 用于原始语言标记翻译
# _l() 针对无法提前评估的文本，进行延迟评估


class LoginForm(FlaskForm):  # 用户登录表单
    """
    Flask-WTF插件不提供字段类型，从WTForms包中导入四个表示表单字段的类。
    每个字段类都接受一个描述或别名作为第一个参数，并生成一个实例来作为LoginForm的类属性。
    可选参数validators用于验证输入字段是否符合预期。
    DataRequired验证器仅验证字段输入是否为空。
    """
    username = StringField(_l('Username'), validators=[DataRequired()])  # 用户名
    password = PasswordField(_l('Password'), validators=[DataRequired()])  # 密码
    remember_me = BooleanField(_l('Remember Me'))  # 复选框
    submit = SubmitField(_l('Sign In'))  # 提交按钮


class RegistrationForm(FlaskForm):  # 用户注册表单
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])  # 双验证器，来自WTForms的Email()验证器确保用户输入的内容同邮件结构匹配
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
