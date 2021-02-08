from django.contrib.auth.models import User
from django import forms
from django.core.mail import send_mail

class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(widget=forms.TextInput)
    enter_password = forms.CharField(widget=forms.PasswordInput)
    retype_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('このユーザーネームはすでに使われています')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('このメールアドレスはすでに使われています')
        return email

    def clean_enter_password(self):
        password = self.cleaned_data.get('enter_password')
        if len(password) < 5:
            raise forms.ValidationError('パスワードは5文字以上で設定してください')
        return password

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('enter_password')
        retyped = self.cleaned_data.get('retype_password')
        if password and retyped and (password != retyped):
            self.add_error('retype_password', 'パスワードが一致しません')

    def send_message(self, email, username):
        from_email = 'withdom.manager@gmail.com'  # 送信者
        subject = "[Withdom]登録確認のお知らせ"
        message = username + "様\nCreHubへのご登録ありがとうございます。\n\n下記内容にてユーザー登録が完了しました\nユーザー名："+username+"\nメールアドレス："+email+"\n\n\n-----------------------------------------------------------------\n発行元：CreHub運営\n問い合わせ先："+from_email
        recipient_list = [email]  # 宛先リスト
        send_mail(subject, message, from_email, recipient_list)

    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('enter_password')
        email = self.cleaned_data.get('email')
        new_user = User.objects.create_user(username = username, email = email)
        new_user.set_password(password)
        new_user.save()
        self.send_message(email, username)
        

