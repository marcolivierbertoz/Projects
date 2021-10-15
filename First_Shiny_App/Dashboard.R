

# Loading the libraries

library(shiny)
library(vroom)
library(tidyverse)
library(lubridate)

# Reading the data
# mass_shooting_df <- vroom::vroom("C:/Users/admin/Desktop/RShiny/Mass_Shooting/mass_shooting_data.csv")

df <- readr::read_csv("mass_shoting_data.csv")
df <- df %>% mutate(`Incident Date` = mdy(`Incident Date`))


ui <- fluidPage(
  titlePanel("Mass Shooting Data - Presentation Generator"),
  fluidRow(
    column(10,
           selectInput("state_select", label = h3("Select a State"), df$State)
           )
  ),
  fluidRow(
    column(10,
           dateRangeInput("dates",label = h3("Select date range"), start=  min(df$`Incident Date`), end= max(df$`Incident Date`))
           )
  ),
  fluidRow(
    column(12,
           plotOutput("event_usa"))
  ),
  fluidRow(
    column(12,
           downloadButton("Presentation","Generate Presentation")
           )
  )
  
)

server <- function(input,output,session){
  
  dateselected <- reactive(df %>% filter(`Incident Date` >= input$dates[1] & `Incident Date` <= input$dates[2]))
  
  selected <- reactive(df %>% filter(State == input$state_select & `Incident Date` >= input$dates[1] & `Incident Date` <= input$dates[2]))
   
  output$event_usa <- renderPlot({
    dateselected() %>% 
    count(Year=year(`Incident Date`)) %>% 
      ggplot(mapping = aes(Year,n))+
      geom_col(fill="White",color="black")+
      geom_text(aes(label=n), position=position_dodge(width=0.9), vjust=-0.25)+
      labs(title="Number of events for the United States of America between the selected dates",
           x="Years",
           y="Number of event")
  })
  
  output$Presentation <- downloadHandler(
    # Selecting output file type
    filename = "Presentation.pptx",
    content = function(file){
      tempReport <- file.path(tempdir(), "Presentation_Template.Rmd")
      file.copy("Presentation_Template.Rmd",tempReport, overwrite = TRUE)
      
      # Setting up the parameters
      params <- list(df = selected(), state=input$state_select, start_date=input$dates[1], end_date=input$dates[2])
      
      # Knitting the document
      rmarkdown::render(tempReport, output_file = file,
                        params = params,
                        envir = new.env(parent =globalenv()))
      
    }
  )
  
  
 
  
}

shinyApp(ui, server)