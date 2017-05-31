#!groovy
podTemplate(label: 'mypod',
            containers: [containerTemplate(name: 'docker', image: 'docker', ttyEnabled: true, command: 'cat')],
            volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')]
  ) {

    node('mypod') {
        def app

        container('docker'){
            stage("Clone Repository"){
                git 'https://github.com/arturoera/picsgrabber_docker.git'
            }
            stage("Build Container"){
                app = docker.build("picsgrabber_tag")
            }
        }


    }
}
// #!groovy
//
// String GIT_VERSION
//
// node {
//     def app
//   // def buildEnv
//   // def devAddress
//
//   stage ('Clone Repository') {
//     checkout scm
//   }
//
//   stage ('Build Image') {
//     // buildEnv = docker.build("build_env:${GIT_VERSION}", 'custom-build-env')
//     app = docker.build("/")
//   }
  //
  // buildEnv.inside {
  //
  //   stage ('Build') {
  //     sh 'sbt compile'
  //     sh 'sbt sampleClient/universal:stage'
  //   }
  //
  //   stage ('Test') {
  //     parallel (
  //       'Test Server' : {
  //         sh 'sbt server/test'
  //       },
  //       'Test Sample Client' : {
  //         sh 'sbt sampleClient/test'
  //       }
  //     )
  //   }
  //
  //   stage ('Prepare Docker Image') {
  //     sh 'sbt server/docker:stage'
  //   }
  // }
  //
  // stage ('Build and Push Docker Image') {
  //   withCredentials([[$class: "UsernamePasswordMultiBinding", usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS', credentialsId: 'Docker Hub']]) {
  //     sh 'docker login --username $DOCKERHUB_USER --password $DOCKERHUB_PASS'
  //   }
  //   def serverImage = docker.build("sambott/grpc-test:${GIT_VERSION}", 'server/target/docker/stage')
  //   serverImage.push()
  //   sh 'docker logout'
  // }
  //
  // stage ('Deploy to DEV') {
  //   devAddress = deployContainer("sambott/grpc-test:${GIT_VERSION}", 'DEV')
  // }
  //
  // stage ('Verify Deployment') {
  //   buildEnv.inside {
  //     sh "sample-client/target/universal/stage/bin/demo-client ${devAddress}"
  //   }
  // }
// }

// stage 'Deploy to LIVE'
//   timeout(time:2, unit:'DAYS') {
//     input message:'Approve deployment to LIVE?'
//   }
//   node {
//     deployContainer("sambott/grpc-test:${GIT_VERSION}", 'LIVE')
//   }
//
// def deployContainer(image, env) {
//   docker.image('lachlanevenson/k8s-kubectl:v1.5.2').inside {
//     withCredentials([[$class: "FileBinding", credentialsId: 'KubeConfig', variable: 'KUBE_CONFIG']]) {
//       def kubectl = "kubectl  --kubeconfig=\$KUBE_CONFIG --context=${env}"
//       sh "${kubectl} set image deployment/grpc-demo grpc-demo=${image}"
//       sh "${kubectl} rollout status deployment/grpc-demo"
//       return sh (
//         script: "${kubectl} get service/grpc-demo -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'",
//         returnStdout: true
//       ).trim()
//     }
//   }
// }
