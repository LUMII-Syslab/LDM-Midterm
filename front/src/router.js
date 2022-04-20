import Vue from "vue";
import Router from "vue-router";
import Projects from "./components/Projects/Projects.vue";
import Project from "./components/Project/Project.vue";
import TrainingData from "./components/TrainingData/TrainingData.vue";
import TestData from "./components/TestData/TestData.vue";
import ValidateData from "./components/ValidateData/ValidateData.vue";

import Run from "./components/Run/Run.vue";
import RunFiles from "./components/RunFiles/RunFiles.vue";
import RunFile from "./components/RunFile/RunFile.vue";

import Login from "./components/Login/Login.vue";
import Users from "./components/Users/Users.vue";
import Profile from "./components/Profile/Profile.vue";
// import TestDataViewer from "./components/TestDataViewer/TestDataViewer.vue";
// import TrainDataViewer from "./components/TrainDataViewer/TrainDataViewer.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "Login",
      meta: {layout: "no-bars"},
      component: require("@/components/Login/Login.vue").default,
    },

    {
      path: "/register",
      name: "Register",
      meta: {layout: "no-bars"},
      component: require("@/components/RegisterUser/RegisterUser.vue").default,
    },

    {
      path: "/projects",
      name: "Projects",
      component: Projects
    },

    {
      path: "/project/:project_id",
      name: "Project",
      component: Project,     
      // props: true
    },

    {
      path: "/training-data/:project_id/:run_id?",
      name: "TrainingData",
      component: TrainingData,     
      // props: true
    },

    {
      path: "/test-data/:project_id/:run_id?",
      name: "TestData",
      component: TestData,
      // props: true
    },

    {
      path: "/validate-data/:project_id/:run_id?",
      name: "ValidateData",
      component: ValidateData,
      // props: true
    },

    { 
      path: '/run-details/:run_id',
      name: "Run",         
      component: Run,       
      // props: true 
    },

    { 
      path: '/run-files/:run_id',
      name: "RunFiles",         
      component: RunFiles,       
      // props: true 
    },

    { 
      path: '/run-file/:run_id/:file_name',
      name: "RunFile",         
      component: RunFile,       
      // props: true 
    },


    {
      path: "/users",
      name: "Users",
      component: Users
    },

    {
      path: "/profile",
      name: "Profile",
      component: Profile
    },

    // { 
    //   path: '/test-data/:project_id',
    //   name: 'TestDataViewer',
    //   component: TestDataViewer,
    //   props: true ,
    //   meta: { requiresAuth: true }
    // },
    // { 
    //   path: '/train-data/:project_id',     
    //   name: 'TrainDataViewer',
    //   component: TrainDataViewer,
    //   props: true ,
    //   meta: { requiresAuth: true },
    // },



    // { 
    //   path: '/addproject/:user_id', 
    //   component: AddProject,   
    //   props: true
    // },    
    // {
    //   path: "/about",
    //   name: "about",
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () =>
    //     import(/* webpackChunkName: "about" */ "./views/About.vue")
    // }
  ]
});




// import Vue from "vue";
// import Router from "vue-router";

// import Login from "./mycomponents/Login/Login.vue";
// import Register from "./mycomponents/RegisterUser/RegisterUser.vue";
// import AppStore from "./mycomponents/AppStore/AppStore.vue";
// import AppDetails from "./mycomponents/AppDetails/AppDetails.vue";
// import AppShelf from "./mycomponents/AppShelf/AppShelf.vue";
// import TaskDetails from "./mycomponents/TaskDetails/TaskDetails.vue";
// import Jobs from "./mycomponents/Jobs/Jobs.vue";
// import JobDetails from "./mycomponents/JobDetails/JobDetails.vue";
// import Profile from "./mycomponents/Profile/Profile.vue";
// import ResourcesShelf from "./mycomponents/ResourcesShelf/ResourcesShelf.vue";
// import DataShelf from "./mycomponents/DataShelf/DataShelf.vue";
// import ResourcesCredits from "./mycomponents/ResourcesCredits/ResourcesCredits.vue";
// import ClusterMachines from "./mycomponents/ClusterMachines/ClusterMachines.vue";
// import Benchmarks from "./mycomponents/Benchmarks/Benchmarks.vue";
// import BenchmarkDetails from "./mycomponents/BenchmarkDetails/BenchmarkDetails.vue";
// import ComputationModules from "./mycomponents/ComputationModules/ComputationModules.vue";
// import ComputationApplications from "./mycomponents/ComputationApplications/ComputationApplications.vue";
// import ComputationModule from "./mycomponents/ComputationModule/ComputationModule.vue";
// import ComputationApplication from "./mycomponents/ComputationApplication/ComputationApplication.vue";
// import Person from "./mycomponents/Person/Person.vue";

// Vue.use(Router);

// export default new Router({
//   routes: [

//     {
//       path: "/",
//       name: "Login",
//       meta: {layout: "no-bars"},
//       component: require("@/mycomponents/Login/Login.vue").default,
//       // component: Login

//     },

//     {
//       path: "/register",
//       name: "Register",
//       meta: {layout: "no-bars"},
//       component: require("@/mycomponents/RegisterUser/RegisterUser.vue").default,
//       // component: Login
//     },

//     {
//       path: "/store",
//       name: "AppStore",
//       component: AppStore
//     },

//     {
//       path: "/app/:id",
//       name: "AppDetails",
//       component: AppDetails
//     },

//     {
//       path: "/app-shelf",
//       name: "AppShelf",
//       component: AppShelf
//     },

//     {
//       path: "/task/:id",
//       name: "TaskDetails",
//       component: TaskDetails
//     },

//     {
//       path: "/jobs",
//       name: "Jobs",
//       component: Jobs
//     },

//     {
//       path: "/job/:id",
//       name: "JobDetails",
//       component: JobDetails
//     },

//     {
//       path: "/profile",
//       name: "Profile",
//       component: Profile
//     },

//     {
//       path: "/resources-shelf",
//       name: "ResourcesShelf",
//       component: ResourcesShelf
//     },

//     {
//       path: "/data-shelf",
//       name: "DataShelf",
//       component: DataShelf
//     },

//     {
//       path: "/cluster-machines/:clusterId",
//       name: "ClusterMachines",
//       component: ClusterMachines
//     },

//     {
//       path: "/benchmarks/:clusterId",
//       name: "Benchmarks",
//       component: Benchmarks
//     },

//     {
//       path: "/benchmark-details/:benchmarkId",
//       name: "BenchmarkDetails",
//       component: BenchmarkDetails
//     },

//     {
//       path: "/resources-credits/:clusterId",      
//       name: "ResourcesCredits",
//       component: ResourcesCredits
//     },

//     {
//       path: "/computation-modules",      
//       name: "ComputationModules",
//       component: ComputationModules
//     },

//     {
//       path: "/development-shelf",      
//       name: "DevelopmentShelf",
//       component: ComputationApplications
//     },

//     {
//       path: "/computation-module/:moduleId",     
//       name: "ComputationModule",
//       component: ComputationModule
//     },

//     {
//       path: "/computation-application/:applicationId",  
//       name: "ComputationApplication",
//       component: ComputationApplication
//     },

//     {
//       path: "/person/:personId",  
//       name: "Person",
//       component: Person
//     },


//   ]

// });
