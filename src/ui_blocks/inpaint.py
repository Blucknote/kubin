import gradio as gr
from utils.gradio_ui import send_gallery_image_to_another_tab, open_another_tab

def inpaint_gallery_select(evt: gr.SelectData):
  return [evt.index, f'Selected image index: {evt.index}']

# TODO: implement region of inpainting
def inpaint_ui(generate_fn, input_i2i_image, input_mix_image_1,  input_mix_image_2, input_inpaint_image, tabs):
  selected_inpaint_image_index = gr.State(None) # type: ignore

  with gr.Row() as inpaint_block:
    with gr.Column(scale=2):
      with gr.Row():
        input_inpaint_image.render()
        with gr.Column():
          prompt = gr.Textbox('hare, 4K photo', label='Prompt')
          negative_prompt = gr.Textbox('bad anatomy, deformed, blurry, depth of field', label='Negative prompt')
      with gr.Row():
        inpainting_target = gr.Radio(['only mask', 'all but mask'], value='only mask', label='Inpainting target')
        inpainting_region = gr.Radio(['whole', 'mask'], value='whole', label='Inpainting region', visible=False)
      with gr.Row():
        steps = gr.Slider(0, 200, 100, step=1, label='Steps')
        guidance_scale = gr.Slider(0, 30, 10, step=1, label='Guidance scale')
      with gr.Row():
        batch_count = gr.Slider(0, 16, 4, step=1, label='Batch count')
        batch_size = gr.Slider(0, 16, 1, step=1, label='Batch size')
      with gr.Row():
        width = gr.Slider(0, 1024, 768, step=1, label='Width')
        height = gr.Slider(0, 1024, 768, step=1, label='Height')
      with gr.Row():
        sampler = gr.Radio(['ddim_sampler', 'p_sampler', 'plms_sampler'], value='p_sampler', label='Sampler')
        seed = gr.Number(-1, label='Seed', precision=0)
      with gr.Row():
        prior_scale = gr.Slider(0, 100, 4, step=1, label='Prior scale')
        prior_steps = gr.Slider(0, 100, 5, step=1, label='Prior steps')
        negative_prior_prompt = gr.Textbox('', label='Negative prior prompt')
    with gr.Column(scale=1):
      generate_inpaint = gr.Button('Generate', variant='primary')
      inpaint_output = gr.Gallery(label='Generated Images').style(grid=2, preview=True)
      selected_image_info = gr.HTML(value='')
      inpaint_output.select(fn=inpaint_gallery_select, outputs=[selected_inpaint_image_index, selected_image_info])

      send_i2i_btn = gr.Button('Send to img2img', variant='secondary')
      send_i2i_btn.click(fn=open_another_tab, inputs=[gr.State(1)], outputs=tabs, # type: ignore
        queue=False).then( 
          send_gallery_image_to_another_tab, inputs=[inpaint_output, selected_inpaint_image_index], outputs=[input_i2i_image] 
        )

      with gr.Row():
        send_mix_1_btn = gr.Button('Send to mix (1)', variant='secondary')
        send_mix_1_btn.click(fn=open_another_tab, inputs=[gr.State(2)], outputs=tabs, # type: ignore
          queue=False).then( 
            send_gallery_image_to_another_tab, inputs=[inpaint_output, selected_inpaint_image_index], outputs=[input_mix_image_1] 
          )
        
        send_mix_2_btn = gr.Button('Send to mix (2)', variant='secondary')
        send_mix_2_btn.click(fn=open_another_tab, inputs=[gr.State(2)], outputs=tabs, # type: ignore
          queue=False).then( 
            send_gallery_image_to_another_tab, inputs=[inpaint_output, selected_inpaint_image_index], outputs=[input_mix_image_2] 
          )
            
      send_inpaint_btn = gr.Button('Send to inpaint', variant='secondary')
      send_inpaint_btn.click(fn=open_another_tab, inputs=[gr.State(3)], outputs=tabs, # type: ignore
        queue=False).then( 
          send_gallery_image_to_another_tab, inputs=[inpaint_output, selected_inpaint_image_index], outputs=[input_inpaint_image] 
        )
      
    generate_inpaint.click(generate_fn, inputs=[
      input_inpaint_image,
      prompt,
      negative_prompt,
      inpainting_target,
      inpainting_region,
      steps,
      batch_count,
      batch_size,
      guidance_scale,
      width,
      height,
      sampler,
      prior_scale,
      prior_steps,
      negative_prior_prompt,
      seed
    ], outputs=inpaint_output)

  return inpaint_block
