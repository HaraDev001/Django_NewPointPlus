<template>
    <v-container class="pa-0">
        <v-row
            no-gutters
            justify="center"
            style="height: 100vh"
            align-content="center"
        >
            <v-col>
                <v-layout justify-center>
                    <v-avatar
                        v-if="isExistCorpImage"
                        color="white"
                        size="120"
                        class="text-center"
                        justify="center"
                    >
                        <img :src="serviceLogoUrl" />
                    </v-avatar>
                    <div v-else>{{ serviceName }}</div>
                </v-layout>
            </v-col>
            <v-col cols="12" class="pa-0 mt-2">
                <div class="text-center">{{ providerName }}</div>
            </v-col>
            <v-col cols="12" md="6" class="mt-8 px-4 py-0">
                <v-form>
                    <v-text-field
                        v-model="form.card.number"
                        placeholder="カード番号"
                        outlined
                        class="mb-4"
                        hide-details="auto"
                        :rules="[]"
                        :error="form.card.error"
                    ></v-text-field>
                    <v-text-field
                        v-model="form.pin.number"
                        placeholder="PIN番号"
                        outlined
                        height="56"
                        class="mb-7"
                        hide-details="auto"
                        :append-icon="
                            form.pin.isMask ? 'visibility' : 'visibility_off'
                        "
                        :type="form.pin.isMask ? 'password' : 'text'"
                        :error="form.pin.error"
                        :error-messages="form.errorMessages"
                        @click:append="form.pin.isMask = !form.pin.isMask"
                    ></v-text-field>
                    <v-btn
                        color="primary"
                        class="white--text font-weight-bold py-4"
                        height="56"
                        block
                        elevation="0"
                        :disabled="form.isInvalid"
                        @click="handleLogin"
                    >
                        ログイン
                    </v-btn>
                </v-form>
            </v-col>
        </v-row>
    </v-container>
</template>
<script lang="ts">
import { getServiceInfo, issueAuthToken } from '../domains/login';
import { Component, Vue, Watch } from 'vue-property-decorator';
import { mapGetters } from 'vuex';

@Component({
    computed: {
        ...mapGetters(['providerName', 'serviceLogoUrl', 'serviceName']),
    },
})
export default class Login extends Vue {
    protected providerName!: string;
    protected serviceLogoUrl!: string;
    protected serviceName!: string;
    form = {
        card: {
            number: '',
            error: false,
        },
        pin: {
            number: '',
            error: false,
            isMask: true,
        },
        isInvalid: true,
        errorMessages: '',
    };
    get formStatus(): string[] {
        return [this.form.card.number, this.form.pin.number];
    }
    get isExistCorpImage(): boolean {
        return Boolean(this.serviceLogoUrl);
    }
    @Watch('formStatus')
    isFilled(): void {
        this.form.card.number && this.form.pin.number
            ? (this.form.isInvalid = false)
            : (this.form.isInvalid = true);
    }
    created(): void {
        this.callGetServiceInfo();
    }
    callGetServiceInfo(): void {
        getServiceInfo().catch((err) => {
            if (err && err.status) {
                if (err.status < 500) {
                    this.$router.push({ name: 'ClientErrorPage' });
                } else {
                    this.$router.push({ name: 'ServerErrorPage' });
                }
            }
        });
    }
    handleLogin(): void {
        issueAuthToken(this.form.card.number, this.form.pin.number)
            .then(() => this.$router.push({ name: 'Top' }))
            .catch((errMsg) => {
                this.form.errorMessages = errMsg;
            });
    }
}
</script>
