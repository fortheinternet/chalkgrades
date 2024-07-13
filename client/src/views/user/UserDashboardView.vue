<script>
  import axios from 'axios'

  // Layouts
  import DashboardLeft from '@/layouts/UserLayout.vue'

  // UI elements
  import Button from '@/components/Button.vue'
  import Loading from '@/components/Loading.vue'
  import Divider from '@/components/Divider.vue'

  export default {
    components: {
      // Layouts
      DashboardLeft,

      // UI elements
      Button,
      Loading,
      Divider
    },
    created() {
      document.title = this.$t('title.Dashboard')

      if (!localStorage.getItem('token')) {
        this.$router.push('/login')
      }

      this.getData()
    },
    data() {
      return {
        requestURL: 'https://chalk.fortheinternet.xyz/api/logins/home.json',
        loading: true,
        responseData: {
          username: '',
          workspaces: {}
        },
        requestData: {
          token: localStorage.getItem('token')
        }
      }
    },
    methods: {
      async getData() {
        try {
          const response = await axios.post(this.requestURL, this.requestData)

          this.loading = false
          this.responseData = response.data
          console.log(this.responseData)
        } catch (error) {
          if (error.response.data.error == 'invalid-token') {
            localStorage.removeItem('token')
            this.$router.push('/login')
          }

          this.$emit('submitted', error.response.data)

          if (error.response) {
            console.table({
              'Error code': error.response.data.error,
              'Error message': error.response.data.message
            })
          } else {
            console.log('Something happened.' + error)
          }
        }
      },
      navigateToWorkspace(work_admin_username, urn, path) {
        this.$router.push(`${work_admin_username}/${urn}/${path}`)
      }
    }
  }
</script>

<template>
  <DashboardLeft view="Dashboard" :username="responseData.username" />
  <main>
    <article>
      <h4>{{ $t('text.heading.dashboard-1') }}</h4>
      <p class="subtext">
        {{ $t('text.paragraph.dashboard-1') }}
      </p>
    </article>

    <Divider />

    <Loading v-if="loading" />

    <div
      class="mb-5 flex select-none flex-row justify-between"
      v-for="workspace in responseData.workspaces"
      v-else
    >
      <div
        class="cursor-pointer"
        @click="
          navigateToWorkspace(
            workspace.work_admin_username,
            workspace.urn,
            'members'
          )
        "
      >
        <p class="mb-0.5 text-[14px] font-bold">{{ workspace.display_name }}</p>
        <p
          class="mb-0 mr-3 inline text-[14px] text-black text-opacity-55 dark:text-white dark:text-opacity-55"
        >
          {{ workspace.work_admin_username }}
        </p>
        <p
          class="mb-0 inline text-[14px] text-black text-opacity-55 dark:text-white dark:text-opacity-55"
        >
          {{ workspace.urn }}
        </p>
      </div>

      <div class="hidden lg:block">
        <div class="button-row">
          <Button
            variant="highlighted"
            @click="
              navigateToWorkspace(
                workspace.work_admin_username,
                workspace.urn,
                'exams'
              )
            "
          >
            {{ $t('button.exams') }}
          </Button>
          <Button
            @click="
              navigateToWorkspace(
                workspace.work_admin_username,
                workspace.urn,
                'members'
              )
            "
          >
            {{ $t('button.members') }}
          </Button>
        </div>
      </div>
    </div>
  </main>
</template>
