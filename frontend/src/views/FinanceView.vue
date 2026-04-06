<template>
  <div class="analytics-container">
    <div class="analytics-tools">

    </div>
    <div class="analytics-graphics">

      <h3>Построение графиков</h3>

      <div class="graphics-choices">
        <input type="checkbox" :disabled="closeDisabled" id="gr-close" value="Close" v-model="checkedGraphs" />
        <label for="gr-close">График цены закрытия</label>

        <input type="checkbox" :disabled="histogramDisabled" id="gr-histogram" value="Histogram" v-model="checkedGraphs" />
        <label for="gr-histogram">Столбчатая диаграмма объемов</label>

        <input type="checkbox" :disabled="candlesDisabled" id="gr-candles" value="Candles" v-model="checkedGraphs" />
        <label for="gr-candles">Японские свечи</label>
      </div>

      <button
        @click="plotGraphs"
        class="plot-button"
        :disabled="loading"
      >
        Построить
      </button>

      <div ref="graphicsContainer" class="graphics">

      </div>
    </div>
  </div>
  </template>

<script>
  import * as echarts from 'echarts';

  export default {
    name: 'FinanceView',

    data(){
      return {
        filename: '',
        loading: false,
        success: false,
        error: null,
        checkedGraphs: [],
      }
    },

    created() {
      this.filename = this.$route.params.filename;
      if (this.filename){
        this.success = true;
      }
      else {
        this.error = 'Файл не был передан.';
      }
    },

    computed: {
      closeDisabled() {
        return this.checkedGraphs.includes('Candles');
      },
      histogramDisabled() {
        return this.checkedGraphs.includes('Candles');
      },
      candlesDisabled() {
        return this.checkedGraphs.includes('Close') || this.checkedGraphs.includes('Histogram');
      },
    },

    methods: {
      async plotGraphs() {
        if (this.checkedGraphs.length < 1) {
          this.error = 'Не выбраны графики';
          return;
        }

        if (!this.filename) {
          this.error = 'Не указано имя файла';
          return;
        }

        this.error = null;
        this.loading = true;

        const requestData = {
          filename: this.filename,
          graphs: this.checkedGraphs
        }

        try {
          const response = await fetch('http://localhost:8000/api/graphics/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(requestData)
          });

          const result = await response.json();
          if (result.status === 'success') {
            this.renderGraphs(result.data)
          } else {
            this.error = result.message;
          }
        } catch (err) {
          this.error = err.message;

        } finally {
          this.loading = false;
        }
      },

      renderGraphs(data) {
        const container = this.$refs.graphicsContainer;
        container.innerHTML = '';

        const graphDiv = document.createElement('div');
        graphDiv.style.width = '100%';
        graphDiv.style.height = '600px';
        container.appendChild(graphDiv);
        const myChart = echarts.init(graphDiv);

        const seriesList = [];
        let xAxisData = null;
        let hasPrice = false;
        let hasVolume = false;

        for (const graphType of this.checkedGraphs){
          const graphData = data[graphType];
          if (!graphData){
            console.warn(`Нет данных для ${graphType}`);
            continue;
          }

          if (!xAxisData && graphData.x) {
            xAxisData = graphData.x;
          }

          if (graphType === 'Close') {
            seriesList.push({
              name: graphData.title,
              yAxisIndex: 0,
              data: graphData.y,
              type: 'line',
              lineStyle: {color: '#4682B4'}

            });
            hasPrice = true;
          }

          else if (graphType === 'Histogram') {
            const onlyOne = (this.checkedGraphs.length === 1);
            seriesList.push({
              name: graphData.title,
              yAxisIndex: onlyOne ? 0 : 1,
              data: graphData.y,
              type: 'bar',
              barWidth: '60%',
              barCategoryGap: '5%',
              itemStyle: {color: '#4682B4'}
            });
            hasVolume = true;
          }

          else if (graphType === 'Candles') {
            let option = {
              title: {
                text: graphData.title
              },
              tooltip: { trigger: 'axis' },
              xAxis: {
                data: graphData.x
              },
              yAxis: {
                type: 'value',
                // min: graphData.ymin,
                // max: graphData.ymax
              },
              series: [
                {
                  type: 'candlestick',
                  data: graphData.y
                }
              ],
              dataZoom: [
                { type: 'slider', start: 0, end: 20 },
                { type: 'inside', start: 0, end: 20 }
              ]
            };
            option && myChart.setOption(option);
          }
        }

        if (seriesList.length === 0) return;

        const yAxisList = [];
        if (hasPrice) {
          yAxisList.push({
            type: 'value',
            name: 'Цена',
            position: 'left',
            alignTicks: true
          });
        }
        if (hasVolume) {
          yAxisList.push({
            type: 'value',
            name: 'Объём',
            position: 'right',
            alignTicks: true,
            axisLabel: { formatter: (value) => value.toLocaleString() }
          });
        }

        if (yAxisList.length === 0) yAxisList.push({ type: 'value' });

        let titleText;
        if (this.checkedGraphs.length === 1) {
          const type = this.checkedGraphs[0];
          titleText = (type === 'Close') ? 'Цена закрытия' : (type === 'Histogram') ? 'Объёмы' : 'График';
        } else {
          titleText = 'Совмещённый график';
        }

        const option = {
          title: { text: titleText },
          tooltip: { trigger: 'axis' },
          legend: { data: seriesList.map(s => s.name) },
          xAxis: {
            type: 'category',
            data: xAxisData,
            name: 'Дата'
          },
          yAxis: yAxisList,
          series: seriesList,
          dataZoom: [
            { type: 'slider', start: 0, end: 20 },
            { type: 'inside', start: 0, end: 20 }
          ]
        };

        myChart.setOption(option);
      },


    }
  }
</script>
