<template>
    <v-app>
        <v-app-bar
            app
            flat
            elevation="1"
            color="transparent"
            class="d-flex justify-center"
        >
            <div class="d-flex align-center">
                <v-img src="~@/assets/cmn/logo.svg" width="132"></v-img>
            </div>
        </v-app-bar>
        <v-container fill-height>
            <v-card max-width="364" class="ma-auto pa-8 pb-12" outlined>
                <v-card-text class="pa-0">
                    <div class="ma-0 pt-1 pb-2 px-0">
                        <v-text-field
                            v-model="user.email"
                            :error="isError"
                            :rules="rules.email"
                            type="text"
                            :label="$t('user.emailAddress')"
                            hide-details="auto"
                            outlined
                            dense
                            maxlength="256"
                        ></v-text-field>
                    </div>

                    <div class="ma-0 pt-2 pb-2 px-0">
                        <v-text-field
                            v-model="user.login_password"
                            :error="isError"
                            :rules="rules.password"
                            :type="isPasswordDisplay ? 'text' : 'password'"
                            hide-details="auto"
                            dense
                            outlined
                            maxlength="100"
                            :label="$t('user.password')"
                            :append-icon="
                                isPasswordDisplay
                                    ? 'visibility_off'
                                    : 'remove_red_eye'
                            "
                            @click:append="
                                isPasswordDisplay = !isPasswordDisplay
                            "
                        ></v-text-field>
                    </div>

                    <span class="red--text" style="white-space: pre-line">
                        {{ message }}
                    </span>
                </v-card-text>
                <v-btn
                    id="login-btn"
                    depressed
                    block
                    large
                    class="mt-5"
                    color="primary"
                    :disabled="!canClick"
                    @click="handleLogin"
                >
                    {{ $t('user.login') }}
                </v-btn>
            </v-card>
        </v-container>
        <layout-footer></layout-footer>
    </v-app>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator';
import LayoutFooter from '../components/Footer.vue';
import { issueAuthToken } from '../domains/login';
import { mapGetters } from 'vuex';

@Component({
    components: { LayoutFooter },
    computed: {
        ...mapGetters(['authToken']),
    },
})
export default class Login extends Vue {
    valid = false;
    isPasswordDisplay = false;
    isError = false;
    isNoInput = false;
    canClick = false;
    private rules = {
        email: [
            (v: string) => !!v || '',
            (v: string) => {
                const pattern =
                    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                return pattern.test(v) || 'メールアドレスが正しくありません。';
            },
        ],
        password: [(v: string) => !!v || ''],
    };

    private user = {
        email: '',
        login_password: '',
        send_email_flag: 1,
    };
    private message = '';
    private redirectFrom: { redirect?: string } = {};
    private authToken!: string;

    created(): void {
        if (this.authToken) {
            this.$router.push({ name: 'History' });
        }
    }

    @Watch('user.email')
    onUserIdChanged(email: string): void {
        this.user.email = email;
        this.changeLoginButtonState();
    }

    @Watch('user.login_password')
    onPasswordChanged(loginPassword: string): void {
        this.user.login_password = loginPassword;
        this.changeLoginButtonState();
    }

    handleLogin(): void {
        issueAuthToken(
            this.user.email,
            this.user.login_password,
            this.user.send_email_flag
        )
            .then(() => {
                this.redirectFrom = this.$route.query;
                if (
                    this.redirectFrom.redirect &&
                    this.redirectFrom.redirect !== '/'
                ) {
                    this.$router.push(this.redirectFrom.redirect);
                } else {
                    this.$router.push({ name: 'History' });
                }
            })
            .catch((errMsg) => {
                this.message = errMsg;
            });
    }

    changeLoginButtonState(): void {
        this.canClick =
            this.isTextInputed(this.user.email) &&
            this.isTextInputed(this.user.login_password);
    }

    isTextInputed(text: string): boolean {
        return text.length > 0 ? true : false;
    }
}
</script>
