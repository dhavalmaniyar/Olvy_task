<template>
    <div class="review">
        <Navbar></Navbar>
        <div class="container">
            <div class="row">
                <div class="col">
                    <h4 class="rfont">Select product ASIN no.</h4>
                </div>
                <div class="col text-end" style="margin-right: 6vw;">
                    <h4 class="rfont">Sort by</h4>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <select
                        @change="onChangeAsin($event)"
                        :required="true"
                        class="form-select rform"
                        name="asin"
                        id="asin"
                    >
                        <option :selected="true">All Data</option>
                        <option
                            v-for="data in productData"
                            v-bind:key="data.product_id"
                            v-bind:value="data.product_id"
                        >{{ data.product_id }}</option>
                    </select>
                </div>
                <div class="col">
                    <select
                        @change="onChangePreference($event)"
                        :required="true"
                        class="form-select float-end rform"
                        name="recent"
                        id="recent"
                    >
                        <option :selected="true" value="topreview">Top Reviews</option>
                        <option value="mostrecent">Most Recent</option>
                    </select>
                </div>
            </div>
        </div>
        <br />
        <br />
        <div class="row">
            <div class="col-md-4 col">
                <div class="card" style="width: 100%; position: sticky;">
                    <div class="card-body" style="position: sticky;">
                        <h5 class="card-title">Customer reviews</h5>
                        <table class="table">
                            <thead></thead>
                            <tbody>
                                <!-- <tr
                                    v-for="(star, index) in starCount.slice().reverse()"
                                    :key="star.index"
                                > -->
                                <!-- {{this.currentStarCountMap}} -->
                                {{productData.ratings   }}
                                <tr v-for="(star,index) in productData.summary" :key="star">
                                    {{index}}
                                     <th scope="row" style="width:15%;">{{index}} Star</th>
                                    <td>
                                        <div class="progress" style="height: 100%;">
                                            <div
                                                class="progress-bar bg-warning"
                                                role="progressbar"
                                                style=" height: 20px;"
                                                v-bind:style="{ 'width': (star * 100 / this.totalStaredReviews) + '%' }"
                                                aria-valuemin="0"
                                                aria-valuemax="100"
                                            ></div>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        {{this.currentStarCountMap}}
                    </div>
                </div>
            </div>
            <div class="col-md-8">
                <div class="container">
                    <div id = "infinite-list-list"
                        v-infinite-scroll="loadMore" infinite-scroll-disabled="busy" infinite-scroll-distance="limit"
                    >
                        <div v-for="data in reviewData" :key="data.id" id = "infinite-list">
                            <div
                                class="card"
                                v-bind:class="data.overall >= 2 ? 'border-success' : 'border-danger'"
                                style="width: 100%"
                            >
                                <div class="card-body">
                                    <table>
                                        <tr>
                                            <td>
                                                <i class="fas fa-user-circle fa-2x"></i>
                                            </td>
                                            <td>
                                                <span>{{ data.reviewerName }}</span>
                                            </td>
                                            <!-- <td><span> <b> {{ data.summary }}</b></span></td> -->
                                        </tr>
                                    </table>
                                    <table>
                                        <tr>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td v-for="index in data.overall" :key="index">
                                                        <i
                                                            class="fas fa-star"
                                                            v-bind:class="data.overall >= 2 ?
                                                            'text-warning' : 'text-danger'"
                                                        ></i>
                                                    </td>
                                                    <td
                                                        v-for="index in starlength - data.overall"
                                                        :key="index"
                                                    >
                                                        <i class="fas fa-star text-secondary"></i>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                        <td>
                                            <table>
                                                <tr>
                                                    <td>
                                                        <span>
                                                            <b>{{ data.summary }}</b>
                                                        </span>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan="2"> <small class="text-muted"> Review Date: {{data.unixReviewTime}}</small></td>
                                        <td></td>
                                    </tr>
                                    </table>
                                    <hr />
                                    <small class="text-muted">Asin no.: {{ data.asin }}</small>
                                    <h6>{{ data.reviewText }}</h6>
                                    <small
                                        class="text-muted"
                                    >{{ data.helpful }} people found this helpful</small>
                                </div>
                            </div>
                            <!-- {{starCount}} -->
                            <br />
                        </div>
                        <!-- <div class="sentinel" ref="sentinel"></div> -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script src="https://unpkg.com/vue-infinite-scroll@2.0.2/vue-infinite-scroll.js"></script>
<script>

import { getAPI } from "../axios-api";
import Vue from 'vue'
import Navbar from "../components/Navbar";
import infiniteScroll from 'vue-infinite-scroll'
Vue.use(infiniteScroll)
export default {
    name: "Review",
    data() {
        return {
            reviewData: [],
            productData: [],
            selectedAsin: [],
            // starCount: [0, 0, 0, 0, 0],
            starlength: 5,
            busy: false,
            limit:5,
            currentPage: 1,
            asinValue:'',
            preferenceValue:'',
            currentStarCountMap: [],
            totalStaredReviews: 0.
        };
    },
    components: {
        Navbar,
    },
    created() {
        getAPI
            .get("/products")
            .then((response) => {
                console.log("Review API has recieved data");
                this.productData = response.data;
                // this.currentStarCountMap = this.productData.ratings;
            })
            .catch((err) => {
                console.log(err);
        });
        // if (asin === "") {
        //     console.log("<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>", this.productData.ratings)
        //     this.currentStarCountMap = this.productData.ratings
        // } else {
        //     productRatings = this.productData.prodStarMap
        //     this.currentStarCountMap = productRatings
        // }
        // console.log("NNEEWWE: >>>> ", this.currentStarCountMap)
        this.loadMore();
    },
    mounted() {
        // this.initialize()
        // this.loadMore
        const listElm = document.querySelector('#infinite-list-list');
        console.log("DKFJKSDF>>>>>>>>>>", listElm)
        listElm.addEventListener('scroll', e => {
            console.log("New >>>>>>>>>>>")
            if(listElm.scrollTop + listElm.clientHeight >= listElm.scrollHeight) {
                console.log(">>>>>>>>>>>>>>>>> ", listElm);
                console.log("ab to ye jitna bhi bole, so jana he");
                this.loadMore();
            }
        });

        // Initially load some items.
        this.loadMore();

        // this.currentStarCountMap = []
        this.updateProductStars(this.asinValue)
        this.updateTotalStarredReviews()
    },
    methods: {
        loadMore() {
            console.log(">>>>>> ", this.asinValue)
            let path = "/review?"
            if (this.preferenceValue !== undefined) {
                path = path + "preference=" + this.preferenceValue
            }

            if (this.asinValue !== undefined && this.asinValue !== "All Data") {
                path = path + "&asin=" + this.asinValue
            }

            console.log("Adding 5 more data results");
            this.busy = true;
            
            getAPI
            .get(path)
            .then(response => {
                console.log("$$$$$$$$$$$$$$",response.data.length)
                const append = response.data.slice(
                    this.reviewData.length,
                    this.reviewData.length + this.limit
                );
                this.reviewData = this.reviewData.concat(append);
                this.busy = false;
            })
            .catch((err) => {
                console.log(err);
            })
        },
        onChangeAsin(event) {
            console.log("!!!!!!!!!!!!!!!" + event.target.value)
            this.asinValue=event.target.value
            this.reviewData = []
            // if (this.asinValue == "All Data") {
            //     console.log("AAA RHA H" + event.target.length)
            //     this.initialize();
            // } else {
                // getAPI
                //     .get("/review?preference=" + this.preferenceValue +"&asin="+this.asinValue )
                //     .then((response) => {
                //         console.log("Review API has recieved data");
                //         this.reviewData = response.data;
                //         // this.starCount = [0, 0, 0, 0, 0]
                //         // this.reviewData.forEach(this.starCountfun)
                //         console.log("DDDDDDDDDDDDDDDDDD", this.reviewData.length)
                //     })
                //     .catch((err) => {
                //         console.log(err);
                //     });
            // }
            console.log(">> caling update: ")
            this.updateProductStars(this.asinValue)
            this.loadMore(this.preferenceValue, this.asinValue)
        },
        updateProductStars(asin) {
            console.log("KLDFSLD", asin)
            // this.currentStarCountMap = []
            if (asin === "All Data" || asin === "") {
                console.log("<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>", this.productData.ratings)
                // this.currentStarCountMap = this.productData.ratings
            } else {
                let productRatings = this.productData.prodStarMap[asin]
                // console.log("<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>New: ", this.productData.prodStarMap)
                // this.currentStarCountMap = productRatings
            }
            this.loadMore();
            this.updateTotalStarredReviews()
        },
        updateTotalStarredReviews() {
            this.totalStaredReviews = 0
            for(let i = 1; i <= 5; i++) {
                this.totalStaredReviews += this.currentStarCountMap[String(i)]
            }
            console.log("Total stars: ", this.totalStaredReviews)
        },
        onChangePreference(event) {
            this.preferenceValue=event.target.value
            this.reviewData = []
            // if (event.target.value == "topreview") {
            //     console.log("AAA RHA H konsa=" + event.target.value)
            //     this.initialize();
            // } else {
                // getAPI
                //     .get("/review?preference="+this.preferenceValue+"&asin="+this.asinValue)
                //     .then((response) => {
                //         console.log("Review API has recieved data");
                //         this.reviewData = response.data;
                //         // this.starCount = [0, 0, 0, 0, 0]
                //         // this.reviewData.forEach(this.starCountfun)
                //         console.log("DDDDDDDDDDDDDDDDDD", this.reviewData.length)
                //     })
                //     .catch((err) => {
                //         console.log(err);
                //     });
            
            this.loadMore(this.preferenceValue, this.asinValue)
        },
        // getReviewData(asin) {
        //     getAPI
        //         .get("/review?asin=" + asin + `&page=${this.currentPage}`)
        //         .then((response) => {
        //             console.log("Review API has recieved data");
        //             this.reviewData = response.data
        //         })
        //         .catch((err) => {
        //             console.log(err);
        //         });
        // },
        // starCountfun: function (store) {
        //     this.starCount[store.overall - 1] += 1
        // },
    },
};  
    // AOS.init();

//   },
//   methods: {
    //   initialize() {
        //     getAPI
        //         .get("/review")
        //         .then((response) => {
        //             console.log("Review API has recieved data");
        //             this.reviewData = response.data;
        //             // this.starCount = [0, 0, 0, 0, 0]
        //             // this.reviewData.forEach(this.starCountfun)
        //             console.log("CCCCCCCCCCCCCC", this.reviewData.length)
        //         })
        //         .catch((err) => {
        //             console.log(err);
        //         });
        // },
        
    // loadMore () {
      
    //   /** This is only for this demo, you could 
    //     * replace the following with code to hit 
    //     * an endpoint to pull in more data. **/
    //   this.loading = true;
    //   setTimeout(e => {
    //     for (var i = 0; i < 20; i++) {
    //       this.items.push('Item ' + this.nextItem++);
    //     }
    //     this.loading = false;
    //   }, 200);
      /**************************************/
      
    // }
//   }
// });

</script>
<style>
.card {
    position: -webkit-sticky;
    position: sticky;
    top: 0;
}
.rfont {
    font-size: 2vh;
}
.rform {
    width: 20vh !important;
}
.scroll-container {
    overflow-y: scroll;
}
</style>