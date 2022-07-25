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
            <v-card min-width="364" class="ma-auto pa-8 pb-12" outlined>
                <p class="text-h6 mb-5">
                    {{ $t('user.changeInitialPassword') }}
                </p>
                <v-card-text class="pa-0">
                    <div class="ma-0 pt-1 pb-1 px-0">
                        <v-text-field
                            v-model="user.password"
                            :error="isError"
                            :type="isCurrentPassword ? 'text' : 'password'"
                            :rules="rules.password"
                            dense
                            hide-details="auto"
                            outlined
                            :label="$t('user.currentPassword')"
                            :append-icon="
                                isCurrentPassword
                                    ? 'visibility_off'
                                    : 'remove_red_eye'
                            "
                            @click:append="
                                isCurrentPassword = !isCurrentPassword
                            "
                        ></v-text-field>
                    </div>

                    <div class="ma-0 pt-3 pb-3 px-0">
                        <v-divider></v-divider>
                    </div>

                    <div class="ma-0 pt-2 pb-2 px-0">
                        <v-text-field
                            v-model="user.newPassword"
                            :error="isError"
                            :type="isNewPassword ? 'text' : 'password'"
                            :rules="rules.password"
                            dense
                            outlined
                            hide-details="auto"
                            :label="$t('user.newPassword')"
                            :append-icon="
                                isNewPassword
                                    ? 'visibility_off'
                                    : 'remove_red_eye'
                            "
                            @click:append="isNewPassword = !isNewPassword"
                        ></v-text-field>
                    </div>

                    <div class="ma-0 pt-2 pb-4 px-0">
                        <v-text-field
                            v-model="user.newConfirmPassword"
                            :error="isError"
                            :type="isConfirmNewPassword ? 'text' : 'password'"
                            dense
                            hide-details="auto"
                            outlined
                            :label="$t('user.newPasswordConfirm')"
                            :append-icon="
                                isConfirmNewPassword
                                    ? 'visibility_off'
                                    : 'remove_red_eye'
                            "
                            :rules="rules.confirmPassword"
                            @click:append="
                                isConfirmNewPassword = !isConfirmNewPassword
                            "
                        ></v-text-field>
                    </div>
                </v-card-text>
                <v-btn
                    class="mt-3"
                    depressed
                    block
                    large
                    color="primary"
                    :disabled="!canClick"
                >
                    {{ $t('common.change') }}
                </v-btn>
            </v-card>
        </v-container>
        <layout-footer></layout-footer>
    </v-app>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator';
import LayoutFooter from '../components/Footer.vue';

@Component({ components: { LayoutFooter } })
export default class InitialPasswordChange extends Vue {
    isCurrentPassword = false;
    isNewPassword = false;
    isConfirmNewPassword = false;
    isError = false;
    isNoInput = false;
    // 入力したパスワードが一致しているか
    isPasswordMatches = false;
    canClick = false;

    private user = {
        password: '',
        newPassword: '',
        newConfirmPassword: '',
    };

    private rules = {
        password: [(v: string) => !!v || 'パスワードが必須です。'],
        confirmPassword: [
            (v: string) => !!v || 'パスワードが必須です。',
            (v: string) =>
                v === this.user.newPassword || 'パスワードが一致しません。',
        ],
    };

    @Watch('user.password')
    onPasswordChanged(password: string): void {
        this.user.password = password;
        this.changeLoginButtonState();
    }

    @Watch('user.newPassword')
    onNewPasswordChanged(newPassword: string): void {
        this.user.newPassword = newPassword;
        this.changeLoginButtonState();
    }

    @Watch('user.newConfirmPassword')
    onConfirmNewPasswordChanged(newConfirmPassword: string): void {
        this.user.newConfirmPassword = newConfirmPassword;
        this.changeLoginButtonState();
    }

    changeLoginButtonState(): void {
        this.canClick =
            this.isTextInputed(this.user.newPassword) &&
            this.isTextInputed(this.user.newConfirmPassword) &&
            this.isTextInputed(this.user.password);
    }

    isTextInputed(text: string): boolean {
        return text.length > 0 ? true : false;
    }
}
</script>
