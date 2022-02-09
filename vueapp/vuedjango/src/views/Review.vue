<template>
    <div class="review">
        <Navbar></Navbar>
        <!-- sort review on the basis of time and helpfulness -->
        <div class="container">
            <div class="row">
                <div class="col">
                    <h4 class="rfont">Select product ASIN no.</h4>
                </div>
                <div class="col text-end" style="margin-right: 6vw;">
                    <h4 class="rfont">Sort by</h4>
                </div>
            </div>
            <!-- get the review of desired product using its aisn no. -->
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
                <!-- summary of the reviews available on the page -->
                <div class="card" style="width: 100%; position: sticky;">
                    <div class="card-body" style="position: sticky;">
                        <h5 class="card-title">Customer reviews</h5>
                        <table class="table">
                            <thead></thead>
                            <tbody>
                                <tr
                                    v-for="(star, index) in starCount.slice().reverse()"
                                    :key="star.id"
                                >
                                    <th scope="row" style="width:15%;">{{ starlength - index }} Star</th>
                                    <td>
                                        <div class="progress" style="height: 100%;">
                                            <div
                                                class="progress-bar bg-warning"
                                                role="progressbar"
                                                style=" height: 20px;"
                                                v-bind:style="{ 'width': (star * 100 / reviewData.length) + '%' }"
                                                aria-valuemin="0"
                                                aria-valuemax="100"
                                            ></div>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div class="col-md-8">
                <!-- review container contains all reviews -->
                <div class="container">
                    <div v-for="data in reviewData" :key="data.id" id="infinite-list">
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
                                        <td colspan="2">
                                            <small
                                                class="text-muted"
                                            >Review Date: {{ data.unixReviewTime }}</small>
                                        </td>
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
                        <br />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>

import { getAPI } from "../axios-api";
import Navbar from "../components/Navbar";
export default {
    name: "Review",
    data() {
        return {
            reviewData: [],
            productData: [],
            selectedAsin: [],
            starCount: [0, 0, 0, 0, 0],
            starlength: 5,
            busy: false,
            limit: 10,
            page: 0,
            asinValue: '',
            preferenceValue: '',
            totalStaredReviews: 0,
        };
    },
    components: {
        Navbar,
    },
    created() { // on page load this function is called to show all available product asin no.
        getAPI
            .get("/products")
            .then((response) => {
                console.log("Review API has recieved data");
                this.productData = response.data;
            })
            .catch((err) => {
                console.log(err);
            });
        this.initialize() //get all reviews form database on loading the page.
    },
    methods: {
        initialize() {
            getAPI
                .get("/review?preference=" + this.preferenceValue + "&asin=" + this.asinValue)
                .then((response) => {
                    console.log("Review API has recieved data");
                    this.testData = response.data
                    this.reviewData = response.data; //reviewData contains the data of based on preferenceValue and asinValue
                    this.starCount = [0, 0, 0, 0, 0]
                    this.reviewData.forEach(this.starCountfun)
                })
                .catch((err) => {
                    console.log(err);
                });
        },
        // for counting the stars per page
        starCountfun: function (store) {
            this.starCount[store.overall - 1] += 1
        },
        // handling on change asin event to get the data
        onChangeAsin(event) {
            this.asinValue = event.target.value
            this.reviewData = []
            if (this.asinValue == "All Data") {
                this.initialize();
            } else {
                getAPI
                    .get("/review?preference=" + this.preferenceValue + "&asin=" + this.asinValue)
                    .then((response) => {
                        console.log("Review API has recieved data");
                        this.reviewData = response.data;
                        this.starCount = [0, 0, 0, 0, 0]
                        this.reviewData.forEach(this.starCountfun)
                    })
                    .catch((err) => {
                        console.log(err);
                    });
            }
        },
        // handling data on the basis of topreview and mostrecent reviews
        onChangePreference(event) {
            this.preferenceValue = event.target.value
            getAPI
                .get("/review?preference=" + this.preferenceValue + "&asin=" + this.asinValue)
                .then((response) => {
                    console.log("Review API has recieved data");
                    this.reviewData = response.data;
                    this.starCount = [0, 0, 0, 0, 0]
                    this.reviewData.forEach(this.starCountfun)
                })
                .catch((err) => {
                    console.log(err);
                });
        },
    },
};
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